#!/usr/bin/python
# -*- coding: UTF-8 -*-

from os import rmdir, path, makedirs
import arcpy


def CalcSVF(in_3D_building, in_3D_point, skyline):
    """Calculate the SVF of a single point
    """
    arcpy.Skyline_3d(in_3D_point, skyline, "", "500 Meters", "0 Meters", in_3D_building, "FULL_DETAIL", "0", "360", "1", "0 Meters", "NO_SEGMENT_SKYLINE", "100", "VERTICAL_ANGLE", "SKYLINE_MAXIMUM", "NO_CURVATURE", "NO_REFRACTION", "0.13", "0", "NO_CREATE_SILHOUETTES")
    arcpy.SkylineGraph_3d(in_3D_point, skyline, "0")
    out_visibility_ratio = float(arcpy.GetMessages().split('degrees is ')[1].split('.\n')[0])

    return out_visibility_ratio


def GetPointsSVF(in_3D_building, in_3D_points, temp_skyline_path):
    """Calculate the SVF of all points and write the attributes
    """
    SVF_dict = {}
    points_cursor = arcpy.SearchCursor(in_3D_points)
    for point in points_cursor:
        FID = point.getValue('FID')
        out_skyline = temp_skyline_path +"/"+ "skyline_"+str(FID)+".shp"
        point_shape = point.getValue('shape')
        out_visibility_ratio = CalcSVF(in_3D_building, point_shape, out_skyline)
        arcpy.Delete_management(out_skyline)
        SVF_dict[FID] = out_visibility_ratio
    
    return SVF_dict


def write_RPE_SVF_table(SVF_actual_dict, SVF_desired_dict, out_RPE_SVF_table):
    """write PE-SVF table by dict
    """
    w_str_list = []
    for FID in SVF_actual_dict:
        DOPid = FID
        DOP_SVF = SVF_desired_dict[FID]
        AOPid = FID
        AOP_SVF = SVF_actual_dict[FID]
        RPE_SVF = abs((AOP_SVF-DOP_SVF)/DOP_SVF*100)
        w_str_list.append(",".join([str(DOPid), str(DOP_SVF), 
            str(AOPid), str(AOP_SVF), str(RPE_SVF)]))

    with open(out_RPE_SVF_table, "w") as w:
        w.write("DOPid,DOP_SVF(10^-2),AOPid,AOP_SVF(10^-2),RPE_SVF(%)\n")
        w.write("\n".join(w_str_list))


def main():
    in_3D_building = arcpy.GetParameterAsText(0)
    in_3D_points_actual = arcpy.GetParameterAsText(1)
    in_3D_points_desired = arcpy.GetParameterAsText(2)
    out_path = arcpy.GetParameterAsText(3)
    if not path.exists(out_path):
        makedirs(out_path)
    out_RPE_SVF_table = "/".join([out_path, "RPESVF.csv"])

    temp_skyline_path = "tempSkylines"
    if not path.exists(temp_skyline_path):
        makedirs(temp_skyline_path)

    SVF_actual_dict = GetPointsSVF(in_3D_building, in_3D_points_actual, temp_skyline_path)
    SVF_desired_dict = GetPointsSVF(in_3D_building, in_3D_points_desired, temp_skyline_path)
    write_RPE_SVF_table(SVF_actual_dict, SVF_desired_dict, out_RPE_SVF_table)
    rmdir(temp_skyline_path)
    print("finish")


if __name__ == '__main__':
    main()
