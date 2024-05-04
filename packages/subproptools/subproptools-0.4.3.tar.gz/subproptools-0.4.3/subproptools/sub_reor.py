"""subreor
Module to reorient a substituent to match a defined coordinate system
First an atom is positioned at the origin.
By convention, this is the atom of the group that is directly bonded to the rest of the molecule.
The rest of the molecule is placed along the -x axis. The remaining axes are defined as follows:
* if there is one lone pair(VSCC), that point lies on the +y
* if there are two lone pairs, the average position of them lies on the +y
* if there are no lone pairs, map the BCPs of the atom at the origin to a reference. Identify the
closest match to the reference to determine a BCP to set as +y

"""
# sys.path.append(sys.path[0].replace("subproptools", "") + "/" + "referenceMaps")
import math  # sqrt
import os

import numpy as np
import pandas as pd  # data frames

from subproptools import (
    qtaim_extract as qt,  # sum file manipulation and property extraction
)
from subproptools.reference_maps import _REFERENCE_MAP

_DEFAULT_STAT_DICT = {
    "rho": {"mean": 0.290686, "sd": 0.077290},
    "lambda1": {"mean": -0.725552, "sd": 0.299756},
    "lambda2": {"mean": -0.678830, "sd": 0.291123},
    "lambda3": {"mean": 0.583261, "sd": 0.449474},
    "DelSqRho": {"mean": -0.821120, "sd": 0.570553},
    "Ellipticity": {"mean": 0.077722, "sd": 0.137890},
    "V": {"mean": -0.475963, "sd": 0.332327},
    "G": {"mean": 0.135342, "sd": 0.184923},
    "H": {"mean": -0.340622, "sd": 0.176627},
    "DI(R,G)": {"mean": 1.081894, "sd": 0.369324},
}


def _get_bcp_reference(originAtom, numBonds):
    """Takes atom and number of bonds and chooses the right map to use."""
    # pylint:disable=too-many-branches
    if originAtom == "C" and numBonds == 4:  # sp3 carbon
        retDict = _REFERENCE_MAP["C"]["sp3"]
    elif originAtom == "C" and numBonds == 3:  # sp2 carbon
        retDict = _REFERENCE_MAP["C"]["sp2"]
        # note linear shouldn't get to this point
    elif originAtom == "B" and numBonds == 3:  # planar boron
        # print('planar boron')
        retDict = _REFERENCE_MAP["B"]["sp2"]
    elif originAtom == "B" and numBonds == 4:  # sp3 boron
        # print('sp3 boron')
        retDict = _REFERENCE_MAP["B"]["sp3"]
    elif originAtom == "N" and numBonds == 4:
        # print('ammonium')
        retDict = _REFERENCE_MAP["N"]["sp3"]
    elif originAtom == "N" and numBonds == 3:
        # print('ammonium')
        retDict = _REFERENCE_MAP["N"]["sp2"]
    elif originAtom == "Al" and numBonds == 3:  # planar aluminum
        retDict = _REFERENCE_MAP["Al"]["sp2"]
    # elif originAtom =='Al' and numBonds==4: #sp3 boron
    #     print('sp3 aluminum')
    elif originAtom == "Si" and numBonds == 4:  # sp3 carbon
        # print('sp3 silicon')
        retDict = _REFERENCE_MAP["Si"]["sp3"]
    elif originAtom == "Si" and numBonds == 3:  # sp2 si
        # print('sp2 silicon')
        retDict = _REFERENCE_MAP["Si"]["sp2"]
    elif originAtom == "P" and numBonds == 4:
        # print('phosphonium')
        retDict = _REFERENCE_MAP["P"]["sp3"]
    elif originAtom == "Se" and numBonds == 4:
        retDict = _REFERENCE_MAP["Se"]["sp3"]
    elif originAtom == "As" and numBonds == 4:
        retDict = _REFERENCE_MAP["As"]["sp3"]
    elif originAtom == "Ge" and numBonds == 4:
        retDict = _REFERENCE_MAP["Ge"]["sp3"]
    elif originAtom == "S" and numBonds == 4:
        retDict = _REFERENCE_MAP["S"]["sp3"]
    return retDict


def _find_bcp_match(data, originAtomXYZ, negXAtomLabel, originAtomLabel, atomDict):
    """
    Finds the atoms connected to the origin atom, and arranges the BCPs in a clockwise sense
    (assuming -x atom going into page)

    Args:
        data: the lines of a .sum file stored as a list
        originAtomXYZ - np.array of xyz coordinates of atom that was to be set to origin
        negXAtomLabel - the atom connected to origin that is positioned along -x axis. e.g. "H2"
        originAtomLabel - the origin atom of substituent bonded to substrate. Format e.g. "C1"

    Returns:
        Dictionary of BCP properties for atoms (non-neg-x atom) that are bonded to the origin atom.
        These are ordered in a clockwise rotational sense
    """

    # find bcps connected to origin atom that are not the -x axis atom
    originBCPs = qt.find_connected(data, negXAtomLabel, originAtomLabel)
    # print(originBCPs)
    bcpPropDict = {}
    # get the bcp properties
    for bcp in originBCPs:
        # bcpBlock = qt.lock()
        bcpPropDict.update(
            {bcp[0] + "-" + bcp[1]: qt.get_bcp_properties(data, atPair=bcp)}
        )
    # print(bcpPropDict)
    if len(bcpPropDict) < 2:
        clockwiseKeys = []
    elif len(bcpPropDict) == 2:
        clockwiseKeys = bcpPropDict
    else:
        clockwiseKeys = _find_clockwise_rot(
            bcpPropDict, originAtomLabel, negXAtomLabel, atomDict, originAtomXYZ
        )
    # at this point have bcpDictionary ordered from 1st to last with clockwise bcp
    return clockwiseKeys  # this is a dictionary of bcps


def _find_clockwise_rot(
    bcpPropDict,
    originAtomLabel,
    negXAtomLabel,
    atomDict,
    originAtomXYZ=np.array([0.0, 0.0, 0.0]),
):
    """given dictionary of bcp properties, find which ones are in a clockwise rotation"""
    # return list of dictionary keys ordered for clockwise rotation
    crossDict = {}

    for key1 in bcpPropDict:
        # print(key1)
        for key2 in bcpPropDict:
            # print(key2)
            if key1 != key2:
                to_rotate = np.vstack(
                    (
                        originAtomXYZ,
                        atomDict[negXAtomLabel]["xyz"],
                        bcpPropDict[key1]["xyz"],
                        bcpPropDict[key2]["xyz"],
                    )
                )

                rot_geom = _set_xaxis(
                    _set_origin(to_rotate, 1),
                    2,
                )
                # zero_3d = np.array([0.0, 0.0, 0.0])
                bcp_1_xyz = rot_geom[2]
                bcp_2_xyz = rot_geom[3]
                bcp_2_xyz[0] = 0.0
                bcp_1_xyz[0] = 0.0
                cross = np.cross(bcp_1_xyz, bcp_2_xyz)[0]
                if cross < 0:
                    bondAt1 = key1.replace(originAtomLabel + "-", "")
                    bondAt1 = bondAt1.replace("-" + originAtomLabel, "")
                    bondAt2 = key2.replace(originAtomLabel + "-", "")
                    bondAt2 = bondAt2.replace("-" + originAtomLabel, "")
                    crossDict.update(
                        {
                            bondAt1
                            + "-To-"
                            + bondAt2: {"Is Clockwise": cross < 0, "cross": cross}
                        }
                    )
    return _order_bcp_dict(crossDict, bcpPropDict)


def _order_bcp_dict(crossDict, bcpPropDict):
    """Take a dictionary of BCPs all connected to one atom and return them sorted in clockwise manner"""
    orderDict = {}
    for cw in crossDict:
        orderDict.update({cw: {"Start": cw.split("-")[0], "End": cw.split("-")[2]}})
    keysList = list(orderDict.keys())
    if len(keysList) == 3:
        if (
            orderDict[keysList[0]]["End"] != orderDict[keysList[1]]["Start"]
            and orderDict[keysList[0]]["End"] == orderDict[keysList[2]]["Start"]
        ):
            reordered_dict = {
                k: orderDict[k] for k in [keysList[0], keysList[2], keysList[1]]
            }
        else:
            reordered_dict = orderDict
        ordered_bcp_props = {}
        for order in reordered_dict:
            for bcp in bcpPropDict:
                # print(bcp)
                if reordered_dict[order]["Start"] in bcp:
                    ordered_bcp_props.update({bcp: bcpPropDict[bcp]})
                    continue
    else:
        ordered_bcp_props = bcpPropDict
    return ordered_bcp_props


def _set_origin(xyzArray, originAtom):
    """shifts all points in xyz geometry by originAtom coordinates, returns xyz geometry

    Args:
        xyzArray: [3XN] np.array where N is number of atoms
        origin Atom: integer label of atom in molecule to be used as origin, starting at 1

    Returns:
        Geometry shifted by setting xyzArray[originAtom-1] as the origin"""
    org = xyzArray[
        originAtom - 1,  # -1 to convert atom index to python starting at 0
    ]
    return xyzArray - org


def _get_lengths(xyzArray):
    """given xyz geometry returns np.array of magnitudes of squared distances from the origin"""
    lengths = np.array([])
    for atom in xyzArray:
        length = 0
        for coord in atom:
            length += coord**2
        lengths = np.append(lengths, length)
    return lengths


def _zero_y_for_negx(t_xyz, negXAtom):
    """perform first rotation in setting -x axis to zero the y value

    Args:
        t_xyz: [Nx3] np.array for N atoms
        negXAtom: integer label of atom to be positioned on -x axis

    Returns:
        [Nx3] rotated geometry with negXAtom on the xz plane
    """
    if t_xyz[0, negXAtom - 1] == 0 and t_xyz[1, negXAtom - 1] == 0:  # on xy
        # print('hi')
        G = np.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]])
    elif (
        t_xyz[1, negXAtom - 1] == 0 and t_xyz[2, negXAtom - 1] == 0
    ):  # already on x axis atom 2 y and z=0
        # print('here')
        G = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    elif t_xyz[0, negXAtom - 1] == 0 and t_xyz[2, negXAtom - 1] == 0:
        # print('ho there')
        G = np.array([[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    else:
        # print('no way')
        d = t_xyz[0, negXAtom - 1] / math.sqrt(
            t_xyz[0, negXAtom - 1] ** 2 + t_xyz[1, negXAtom - 1] ** 2
        )
        s = t_xyz[1, negXAtom - 1] / math.sqrt(
            t_xyz[0, negXAtom - 1] ** 2 + t_xyz[1, negXAtom - 1] ** 2
        )
        G = np.array([[d, s, 0.0], [-s, d, 0.0], [0.0, 0.0, 1.0]])
    return np.matmul(G, t_xyz)


def _zero_z_for_negx(t_xyz, negXAtom):
    """perform second rotation in setting -x axis to zero the z value

    Args:
        t_xyz: [Nx3] np.array for N atoms
        negXAtom: integer label of atom to be positioned on -x axis

    Returns:
        [Nx3] rotated geometry with negXAtom on the x acis(may be + or -)"""
    # perform after y
    d = t_xyz[0, negXAtom - 1] / math.sqrt(
        t_xyz[0, negXAtom - 1] ** 2 + t_xyz[2, negXAtom - 1] ** 2
    )
    s = t_xyz[2, negXAtom - 1] / math.sqrt(
        t_xyz[0, negXAtom - 1] ** 2 + t_xyz[2, negXAtom - 1] ** 2
    )
    G = np.array([[d, 0, s], [0, 1, 0], [-s, 0, d]])
    return np.matmul(G, t_xyz)


def _set_xaxis(xyzArray, negXAtom):
    """Given xyz geometry with atom at origin, areturn xyz geometry with negXAtom on -x.

    Args:
        xyzArray: [3xN] np.array for N atoms of geometry
        negXAtom: integer label of atom to be positioned on -x axis

    Returns:
        [Nx3] rotated geometry with negXAtom on the xz plane
    """
    t_xyz = xyzArray.T

    # define initial xyz vector lengths. Should be unchanged after rotation
    tol = 0.0001  # tolerance for change
    initial_lengths = _get_lengths(xyzArray)
    t_rot1 = _zero_y_for_negx(t_xyz, negXAtom)
    rot1_lengths = _get_lengths(t_rot1.T)
    if np.any((rot1_lengths - initial_lengths) > tol):
        raise AssertionError("Geometry change after rotation exceeded tolerance")
    t_rot2 = _zero_z_for_negx(t_rot1, negXAtom)
    rot2_lengths = _get_lengths(t_rot2.T)

    if np.any((rot2_lengths - initial_lengths) > tol):
        raise AssertionError("Geometry change after rotation exceeded tolerance")
    if t_rot2[0, negXAtom - 1] > 0:  # if negxatom is along +x, rotate 180
        G = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])
        t_rot_final = np.matmul(G, t_rot2)
        return t_rot_final.T
    return t_rot2.T


def _popelier_match_scores_2(testDict, refDict, statDict):
    """Calculate QTMS differences between BCP dictionaries"""
    refDictKeysList = list(refDict.keys())
    testKeysList = list(testDict.keys())
    # BCP distances for first match
    dif00 = _get_popelier_dif(
        testDict[testKeysList[0]], refDict[refDictKeysList[0]], statDict
    )
    dif11 = _get_popelier_dif(
        testDict[testKeysList[1]], refDict[refDictKeysList[1]], statDict
    )

    # BCP distances for second match
    dif10 = _get_popelier_dif(
        testDict[testKeysList[1]], refDict[refDictKeysList[0]], statDict
    )

    # BCP distances for third match

    dif01 = _get_popelier_dif(
        testDict[testKeysList[0]], refDict[refDictKeysList[1]], statDict
    )

    return [dif00 + dif11, dif10 + dif01]
    # Total score list and index of closest space


def _popelier_match_scores(testDict, refDict, statDict):
    """Calculate QTMS differences between BCP dictionaries"""
    refDictKeysList = list(refDict.keys())
    testKeysList = list(testDict.keys())
    # BCP distances for first match
    dif00 = _get_popelier_dif(
        testDict[testKeysList[0]], refDict[refDictKeysList[0]], statDict
    )
    dif11 = _get_popelier_dif(
        testDict[testKeysList[1]], refDict[refDictKeysList[1]], statDict
    )
    dif22 = _get_popelier_dif(
        testDict[testKeysList[2]], refDict[refDictKeysList[2]], statDict
    )
    # BCP distances for second match
    dif10 = _get_popelier_dif(
        testDict[testKeysList[1]], refDict[refDictKeysList[0]], statDict
    )
    dif21 = _get_popelier_dif(
        testDict[testKeysList[2]], refDict[refDictKeysList[1]], statDict
    )
    dif02 = _get_popelier_dif(
        testDict[testKeysList[0]], refDict[refDictKeysList[2]], statDict
    )
    # BCP distances for third match
    dif20 = _get_popelier_dif(
        testDict[testKeysList[2]], refDict[refDictKeysList[0]], statDict
    )
    dif01 = _get_popelier_dif(
        testDict[testKeysList[0]], refDict[refDictKeysList[1]], statDict
    )
    dif12 = _get_popelier_dif(
        testDict[testKeysList[1]], refDict[refDictKeysList[2]], statDict
    )
    return [dif00 + dif11 + dif22, dif10 + dif21 + dif02, dif20 + dif01 + dif12]
    # Total score list and index of closest space


def _align_dicts_2(testDict, refDict, statDict):
    """
    Arguments:
        testDict and refDict:For two dictionaries that are ordered in same rotational sense
        statDict: scaling to use
    Returns:
        np.array of xyz point to use
    """
    # pylint:disable=too-many-branches
    matchScores = _popelier_match_scores_2(testDict, refDict, statDict)
    refDictKeysList = list(refDict.keys())
    testKeysList = list(testDict.keys())
    minInd = matchScores.index(min(matchScores))

    # identify the refDict BCP that is on the +y axis
    if (
        refDict[refDictKeysList[0]]["xyz"][1] > 0
        and abs(refDict[refDictKeysList[0]]["xyz"][2]) < 0.01
    ):
        refPosY = 0
    elif (
        refDict[refDictKeysList[1]]["xyz"][1] > 0
        and abs(refDict[refDictKeysList[1]]["xyz"][2]) < 0.01
    ):
        refPosY = 1

    # for the best match, set the posYPoint to the one that mapped to refDict +y point
    # if first element of match scores, 0 of ref maps to 0 of test. If second element,
    # 1 of ref maps to 0 of test
    if minInd == 0:
        if refPosY == 0:
            posYPoint = testDict[testKeysList[0]]["xyz"]
        elif refPosY == 1:
            posYPoint = testDict[testKeysList[1]]["xyz"]

    elif minInd == 1:
        if refPosY == 0:
            posYPoint = testDict[testKeysList[1]]["xyz"]
        elif refPosY == 1:
            posYPoint = testDict[testKeysList[0]]["xyz"]

    # elif minInd == 2:
    #     if refPosY == 0:
    #         posYPoint = testDict[testKeysList[2]]["xyz"]
    #     elif refPosY == 1:
    #         posYPoint = testDict[testKeysList[0]]["xyz"]

    return posYPoint


def _align_dicts(testDict, refDict, statDict):
    """
    Arguments:
        testDict and refDict:For two dictionaries that are ordered in same rotational sense
        statDict: scaling to use
    Returns:
        np.array of xyz point to use
    """
    # pylint:disable=too-many-branches
    matchScores = _popelier_match_scores(testDict, refDict, statDict)
    refDictKeysList = list(refDict.keys())
    testKeysList = list(testDict.keys())
    minInd = matchScores.index(min(matchScores))

    # identify the refDict BCP that is on the +y axis
    if (
        refDict[refDictKeysList[0]]["xyz"][1] > 0
        and abs(refDict[refDictKeysList[0]]["xyz"][2]) < 0.01
    ):
        refPosY = 0
    elif (
        refDict[refDictKeysList[1]]["xyz"][1] > 0
        and abs(refDict[refDictKeysList[1]]["xyz"][2]) < 0.01
    ):
        refPosY = 1
    elif (
        refDict[refDictKeysList[2]]["xyz"][1] > 0
        and abs(refDict[refDictKeysList[2]]["xyz"][2]) < 0.01
    ):
        refPosY = 2
    # for the best match, set the posYPoint to the one that mapped to refDict +y point
    if minInd == 0:
        if refPosY == 0:
            posYPoint = testDict[testKeysList[0]]["xyz"]
        elif refPosY == 1:
            posYPoint = testDict[testKeysList[1]]["xyz"]
        elif refPosY == 2:
            posYPoint = testDict[testKeysList[2]]["xyz"]
    elif minInd == 1:
        if refPosY == 0:
            posYPoint = testDict[testKeysList[1]]["xyz"]
        elif refPosY == 1:
            posYPoint = testDict[testKeysList[2]]["xyz"]
        elif refPosY == 2:
            posYPoint = testDict[testKeysList[0]]["xyz"]
    elif minInd == 2:
        if refPosY == 0:
            posYPoint = testDict[testKeysList[2]]["xyz"]
        elif refPosY == 1:
            posYPoint = testDict[testKeysList[0]]["xyz"]
        elif refPosY == 2:
            posYPoint = testDict[testKeysList[1]]["xyz"]
    return posYPoint


def _get_posy_point_aiida(
    data, cc_dict, atomDict, attachedAtom, negXAtomLabel, default_stats=True
):
    # pylint:disable=too-many-arguments
    # ccProps = qt.get_cc_props(FolderData,attachedAtom,is_folder_data=True)
    for key in list(cc_dict.keys()):
        keynum = int("".join(filter(str.isdigit, key)))
        if keynum == 1:
            vscc = cc_dict[key]
    # if len(ccProps) > 0:
    #     vscc = qt.identify_vscc(ccProps,atomDict,attachedAtom)
    # else:
    #     vscc = {}
    if len(vscc) == 1:  # pylint:disable=used-before-assignment
        # reorient setting vscc to +y
        vkeys = list(vscc.keys())
        posYPoint = vscc[vkeys[0]]["xyz"]
    elif len(vscc) == 2 and "N" not in attachedAtom:
        vkeys = list(vscc.keys())

        posYPoint = [
            x / 2
            for x in [
                vscc[vkeys[0]]["xyz"][0] + vscc[vkeys[1]]["xyz"][0],
                vscc[vkeys[0]]["xyz"][1] + vscc[vkeys[1]]["xyz"][1],
                vscc[vkeys[0]]["xyz"][2] + vscc[vkeys[1]]["xyz"][2],
            ]
        ]
        # reorient to average of vscc points for +y
    else:
        # bcpsToMatch is bcp dictionary, ordered for clockwise rot
        # data,originAtomXYZ,negXAtomLabel,originAtomLabel
        bcpsToMatch = _find_bcp_match(
            data, atomDict[attachedAtom]["xyz"], negXAtomLabel, attachedAtom, atomDict
        )
        # on the assumption that if an atom has two bonds (_find_bap_match returns None),
        # and does not have a lone pair, it is linear, so we do not do another rotation
        # and posYPoint is None
        if len(bcpsToMatch) == 0 or len(bcpsToMatch) == 1:
            posYPoint = []
        else:
            atType = "".join([i for i in attachedAtom if not i.isdigit()])
            matchDict = _get_bcp_reference(atType, len(bcpsToMatch) + 1)
            if default_stats:
                statDict = _DEFAULT_STAT_DICT
            if len(bcpsToMatch) == 3:
                posYPoint = _align_dicts(bcpsToMatch, matchDict, statDict)
            elif len(bcpsToMatch) == 2:
                posYPoint = _align_dicts_2(bcpsToMatch, matchDict, statDict)
        # reorient to another point
        # posy point will be the point that would lie along the y-axis in reference in maximal match case
        # print('not done yet')
    return posYPoint


def _get_posy_point(
    sumFileNoExt, atomDict, attachedAtom, negXAtomLabel, default_stats=True
):
    """returns point to put on +y axis matching definition in rotate_substituent."""
    ccProps = qt.get_cc_props(sumFileNoExt, attachedAtom)
    if len(ccProps) > 0:
        vscc = qt.identify_vscc(ccProps, atomDict, attachedAtom)
    else:
        vscc = {}
    if len(vscc) == 1:
        # reorient setting vscc to +y
        vkeys = list(vscc.keys())
        posYPoint = vscc[vkeys[0]]["xyz"]
    elif len(vscc) == 2 and "N" not in attachedAtom:
        vkeys = list(vscc.keys())

        posYPoint = [
            x / 2
            for x in [
                vscc[vkeys[0]]["xyz"][0] + vscc[vkeys[1]]["xyz"][0],
                vscc[vkeys[0]]["xyz"][1] + vscc[vkeys[1]]["xyz"][1],
                vscc[vkeys[0]]["xyz"][2] + vscc[vkeys[1]]["xyz"][2],
            ]
        ]
        # reorient to average of vscc points for +y
    else:
        with open(sumFileNoExt + ".sum", encoding="utf-8") as sumFile:
            # sumFile = open()
            data = sumFile.readlines()
        # sumFile.close()
        # bcpsToMatch is bcp dictionary, ordered for clockwise rot
        # data,originAtomXYZ,negXAtomLabel,originAtomLabel
        bcpsToMatch = _find_bcp_match(
            data, atomDict[attachedAtom]["xyz"], negXAtomLabel, attachedAtom, atomDict
        )
        # on the assumption that if an atom has two bonds (_find_bap_match returns None),
        # and does not have a lone pair, it is linear, so we do not do another rotation
        # and posYPoint is None
        if len(bcpsToMatch) == 0 or len(bcpsToMatch) == 1:
            posYPoint = []
        else:
            atType = "".join([i for i in attachedAtom if not i.isdigit()])
            matchDict = _get_bcp_reference(atType, len(bcpsToMatch) + 1)
            if default_stats:
                statDict = _DEFAULT_STAT_DICT
            if len(bcpsToMatch) == 3:
                posYPoint = _align_dicts(bcpsToMatch, matchDict, statDict)
            elif len(bcpsToMatch) == 2:
                posYPoint = _align_dicts_2(bcpsToMatch, matchDict, statDict)
        # reorient to another point
        # posy point will be the point that would lie along the y-axis in reference in maximal match case
        # print('not done yet')
    return posYPoint


def _set_yaxis(xyzArray, posYArray):
    """rotate a geom positioned on -x axis so posYArray will lie on +y"""
    theta = math.atan2(posYArray[2], posYArray[1])
    # print(theta)
    c = math.cos(theta)
    s = math.sin(theta)
    G = np.array([[1, 0, 0], [0, c, s], [0, -s, c]])
    rot1 = np.matmul(G, xyzArray.T)
    rot1vec = np.matmul(G, posYArray)

    if rot1vec[1] < 0:
        G2 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
        final_geom = np.matmul(G2, rot1)
    else:
        final_geom = rot1
    return final_geom.T


def _get_popelier_dif(bcpDictA, bcpDictB, statDict):
    """compute distance in BCP space between dictA and B scaling using statDict"""
    distancesq = 0.0
    for prop in bcpDictA:
        if prop != "xyz":
            scaledA = (bcpDictA[prop][0] - statDict[prop]["mean"]) / statDict[prop][
                "sd"
            ]
            scaledB = (bcpDictB[prop][0] - statDict[prop]["mean"]) / statDict[prop][
                "sd"
            ]
            distancesq += (scaledA - scaledB) ** 2
    return math.sqrt(distancesq)


def rotate_substituent_aiida(
    sum_file_folder, atom_dict, cc_dict, originAtom=1, negXAtom=2, posYAtom=0
):
    # pylint:disable=too-many-arguments
    """
    Rotates a substituent to the defined coordinate system.

    Args:
        sum_file_folder (aiida FolderData): FolderData  object containing .sum file
        atom_dict: dict of output from get_atomic_props
        cc_dict: dict of VSCC data
        originAtom (int): the integer number of the atom to place at the origin
        negXAtom (int): the integer number of the atom to place along the -x axis
        posYAtom (int): override for above defined +y point, set to posYAtom instead

    Returns:
        dictionary 'atomic_symbols' for atomic symbols and 'geom' for 3xN np.array of rotated coordinates

    Examples:
        >>> rotate_substituent('SubCH3_CFH2_anti2146_reor',1,2)
        Atom    x   y   z
        C1      0.  0.  0.
        H2 -{float} 0.  0.
        .(remaining geometry)
        .
        .

    Notes:
        Coordinate system defined as:
        originAtom at (0,0,0)
        negXAtom at (-x,0,0)
        Atom on +y defined as:
        average of lone pairs for 2 lone pairs on originAtom
        Position of lone pair for 1 lone pair on originAtom
        For no lone pairs: map BCPs onto reference for the atom type
        Minimum distance in BCP space defined the atom to put on +y

    """
    # pylint:disable=too-many-locals
    # read sum file
    data = sum_file_folder.get_object_content("aiida.sum").split("\n")

    molecule_xyz = qt.get_xyz(data)
    # Labels format A1 etc
    negXAtomLabel = molecule_xyz["Atoms"][negXAtom - 1]
    attachedAtom = molecule_xyz["Atoms"][originAtom - 1]
    if not posYAtom and len(molecule_xyz["Atoms"]) > 2:
        posYPoint = _get_posy_point_aiida(
            data, cc_dict, atom_dict, attachedAtom, negXAtomLabel
        )
    else:
        posYPoint = []
    if len(posYPoint) > 0:
        xyz_w_y_pt = np.append(molecule_xyz["xyz"], [posYPoint], axis=0)
        # perform reorientation
        molecule_xaxis = _set_xaxis(_set_origin(xyz_w_y_pt, originAtom), negXAtom)
        final_y = molecule_xaxis[posYAtom - 1]
        final_orientation = _set_yaxis(molecule_xaxis[0:-1], final_y)
    elif posYAtom:
        posYPoint = molecule_xyz["xyz"][posYAtom - 1]
    else:
        molecule_xaxis = _set_xaxis(
            _set_origin(molecule_xyz["xyz"], originAtom), negXAtom
        )
        final_orientation = molecule_xaxis
    # Generate output
    final_orientation = final_orientation * 0.529177
    # outFrame = pd.DataFrame(final_orientation*0.529177,columns = ['x','y','z'])
    # outFrame['Atom'] = molecule_xyz['Atoms']
    # outFrame = outFrame[['Atom','x','y','z']]
    num_nna = len([x for x in molecule_xyz["Atoms"] if "NNA" in x])
    tot_num_ats = len(molecule_xyz["Atoms"])

    # out_dict = {molecule_xyz['Atoms'][i]:final_orientation[i] for i in range(0,len(molecule_xyz['Atoms']))}
    return {
        "atom_symbols": molecule_xyz["Atoms"][0 : (tot_num_ats - num_nna)],
        "geom": final_orientation[0 : (tot_num_ats - num_nna)],
    }


def rotate_substituent(sumFileNoExt, originAtom, negXAtom, posYAtom=0):
    """
    Rotates a substituent to the defined coordinate system.

    Args:
        sumFileNoExt (string): name of a sum file, without the .sum extension
        originAtom (int): the integer number of the atom to place at the origin
        negXAtom (int): the integer number of the atom to place along the -x axis
        posYAtom (int): override for above defined +y point, set to posYAtom instead

    Returns:
        pandas data frame of output geometry (columns Atom, x, y, z)

    Examples:
        >>> rotate_substituent('SubCH3_CFH2_anti2146_reor',1,2)
        Atom    x   y   z
        C1      0.  0.  0.
        H2 -{float} 0.  0.
        .(remaining geometry)
        .
        .

    Notes:
        Coordinate system defined as:
        originAtom at (0,0,0)
        negXAtom at (-x,0,0)
        Atom on +y defined as:
        average of lone pairs for 2 lone pairs on originAtom
        Position of lone pair for 1 lone pair on originAtom
        For no lone pairs: map BCPs onto reference for the atom type
        Minimum distance in BCP space defined the atom to put on +y

    """
    # pylint:disable=too-many-locals
    # read sum file
    with open(sumFileNoExt + ".sum", encoding="utf-8") as sumFile:
        # sumFile = open(sumFileNoExt + ".sum")
        data = sumFile.readlines()
    # sumFile.close()
    atomDict = qt.get_atomic_props(data)  # (needed for VSCC identification)

    molecule_xyz = qt.get_xyz(data)
    # Labels format A1 etc
    negXAtomLabel = molecule_xyz["Atoms"][negXAtom - 1]
    attachedAtom = molecule_xyz["Atoms"][originAtom - 1]
    # perform reorientation
    if not posYAtom and len(molecule_xyz["Atoms"]) > 2:
        posYPoint = _get_posy_point(sumFileNoExt, atomDict, attachedAtom, negXAtomLabel)
    elif posYAtom:
        posYPoint = molecule_xyz["xyz"][posYAtom - 1]
    else:
        posYPoint = []
    if len(posYPoint) > 0:
        print(molecule_xyz["xyz"])
        print(posYPoint)
        xyz_w_y_pt = np.append(molecule_xyz["xyz"], [posYPoint], axis=0)
        # perform reorientation
        molecule_xaxis = _set_xaxis(_set_origin(xyz_w_y_pt, originAtom), negXAtom)
        final_y = molecule_xaxis[posYAtom - 1]
        final_orientation = _set_yaxis(molecule_xaxis[0:-1], final_y)
    else:
        molecule_xaxis = _set_xaxis(
            _set_origin(molecule_xyz["xyz"], originAtom), negXAtom
        )
        final_orientation = molecule_xaxis

    # Generate output
    outFrame = pd.DataFrame(final_orientation * 0.529177, columns=["x", "y", "z"])
    outFrame["Atom"] = molecule_xyz["Atoms"]
    outFrame = outFrame[["Atom", "x", "y", "z"]]

    return outFrame


def output_to_gjf(
    # pylint:disable=too-many-arguments
    old_file_name,
    reor_geom,
    esm="wB97XD",
    basis_set="aug-cc-pvtz",
    add_label="",
    n_procs=4,
    mem="3200MB",
    charge=0,
    multiplicity=1,
    wfx=True,
):
    """Given a rotated molecule, writes new geometry to single point Gaussian calculation

    Args:
        old_file_name - the file name of the sum file(no extension) before reorientation
        reor_geom - the data frame output of rotate_substituent
        esm - whatever electronic structure method is to be used in single point(HF/MP2/functional)
        basis_set - basis set to be used
        add_label - any extra label for file name, default empty
        n_procs=4 - numper of processors for remote clusters, set to 0 if not desired
        mem='3200MB' -amount of memory for remote clusters, set to 0 if not desired
        charge - charge of molecule
        multiplicity - multiplicity of molecule
        wfx - whether or not to write wfx, default True

    Returns:
        no return, but creates new gjf file old_file_name_reor_add_label.gjf
        File looks like:
        %chk=new_file_name.chk
        %nprocs=n_procs
        %mem=mem
        #p esm/basis_set output=wfx nosymmetry

        single point on old_file reoriented by subproptools

        charge multiplicity
        (xyz geom)

        new_file_name.wfx
        (blank lines)
    """
    new_file_name = old_file_name + "_reor" + add_label
    # delete file if already exists
    if os.path.exists(new_file_name + ".gjf"):
        # print('deleting')
        os.remove(new_file_name + ".gjf")
    chk_name = new_file_name + ".chk"
    with open(new_file_name + ".gjf", "a", encoding="utf-8") as f:
        f.write(f"%chk={chk_name}\n")
        if n_procs:
            f.write(f"%nprocs={n_procs}\n")
        if mem:
            f.write(f"%mem={mem}\n")
        if wfx:
            f.write(f"#p {esm}/{basis_set} output=wfx nosymmetry\n")
        else:
            f.write(f"#p {esm}/{basis_set} nosymmetry\n")
        f.write("\n")
        f.write(f"single point on {old_file_name} reoriented by subproptools\n")
        f.write("\n")
        f.write(f"{charge} {multiplicity}\n")
        dfAsString = reor_geom.to_string(header=False, index=False)
        f.write(
            dfAsString.split("NNA")[0]
        )  # NNAs are appended as last atom - don't write them
        if "NNA" not in dfAsString:
            f.write("\n\n")
        else:
            f.write("\n")
        if wfx:
            f.write(new_file_name + ".wfx\n\n\n")
        else:
            f.write("\n\n\n")


def rotate_sheet(
    csv_file, esm, basis, n_procs=4, mem="3200MB", wfx=True, extra_label=""
):
    """
    Given csv file and Gaussian calculation options, reorient files in csv_file and output gjf

    Args:
        csv_file - csv file containining these columns:
        Substituent, originAtom, negXAtom, posYAtom, charge, multiplicity,  label1, label2,...
        Substituent: string label for substituent
        originAtom: numerical index(starting form 1) of atom to use as origin
        negXAtom: numerical index(starting form 1) of atom to place on -x
        posYAtom: usually 0, but override if desired, numerical index(starting form 1) of atom to place on +y
        charge: charge of the molecule
        multiplicity: multiplicity of the molecule
        label1, label2... label depicting situation for molecule(substrate, method) e.g. "SubH", "B3LYP/cc-pvDZ" etc
        esm: electronic structure method (HF/MP2/DFT functional/etc)
        basis: string for basis to be used
        n_procs: number of processors for use on Cedar, default to 4
        mem: memory to use on Cedar, default to 3200MB
        wfx: if we wish to write wfx, default True
        extra_label: an additional label for the reoriented file if needed, default none

    Returns:
        no return value, but outputs to gjf files in working directory(or directory in path of filenames)

    """
    # pylint:disable=too-many-arguments
    # pylint:disable=too-many-locals
    csvFrame = pd.read_csv(csv_file)
    ncolumns = csvFrame.shape[1]
    nrow = csvFrame.shape[0]
    for sub in range(0, nrow):
        charge = csvFrame["charge"][sub]
        multiplicity = csvFrame["multiplicity"][sub]
        originAtom = csvFrame["originAtom"][sub]
        negXAtom = csvFrame["negXAtom"][sub]
        posYAtom = csvFrame["posYAtom"][sub]
        for label in range(6, ncolumns):
            rot_file = csvFrame.iloc[sub, label]
            print(f"""Rotating {rot_file}""")
            rot_geom = rotate_substituent(
                rot_file, originAtom=originAtom, negXAtom=negXAtom, posYAtom=posYAtom
            )
            print(f"""Creating new Gaussian gjf for {rot_file}""")
            output_to_gjf(
                rot_file,
                rot_geom,
                esm=esm,
                basis_set=basis,
                add_label=extra_label,
                n_procs=n_procs,
                mem=mem,
                charge=charge,
                multiplicity=multiplicity,
                wfx=wfx,
            )


# commented out - have included reference bcps at data at top of file rather tahn calculating each time
def _get_ref_bcps(
    sumfilenoext,
    atPairList,
    originAtom,
    negXAtomLabel,
    originAtomXYZ=np.array([0.0, 0.0, 0.0]),
):
    """given reference sumfile, extract bcp properties for needed bcps"""
    # sumFile = open(sumfilenoext + ".sum")  # open file, read lines, close file
    with open(sumfilenoext + ".sum", encoding="utf-8") as sumFile:
        data = sumFile.readlines()
    # sumFile.close()
    atomDict = qt.get_atomic_props(data)
    bcpDict = {}
    for bcp in atPairList:
        # block = qt.get_bcp_block(data,bcp)
        bcpDict.update({f"{bcp[0]}-{bcp[1]}": qt.get_bcp_properties(data, bcp)})
    clockbcpDict = _find_clockwise_rot(
        bcpDict, originAtom, negXAtomLabel, atomDict, originAtomXYZ
    )
    return clockbcpDict
