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
    calc_SVF_name = "SVF"
    field_name_list = [f.name for f in arcpy.ListFields(in_3D_points)]
    if calc_SVF_name not in field_name_list:
        arcpy.AddField_management(in_3D_points, calc_SVF_name, "DOUBLE")
    
    SVF_dict = {}
    points_cursor = arcpy.UpdateCursor(in_3D_points)
    for point in points_cursor:
        FID = point.getValue('FID')
        out_skyline = temp_skyline_path +"/"+ "skyline_"+str(FID)+".shp"
        point_shape = point.getValue('shape')
        out_visibility_ratio = CalcSVF(in_3D_building, point_shape, out_skyline)
        point.setValue("SVF", out_visibility_ratio)
        points_cursor.updateRow(point)
        arcpy.Delete_management(out_skyline)
        SVF_dict[FID] = out_visibility_ratio
    
    return SVF_dict

def write_SVF_table(SVF_dict, out_SVF_table):
    """write SVF table by dict
    """
    w_str_list = [",".join([str(FID), str(SVF_dict[FID])]) 
        for FID in SVF_dict]

    with open(out_SVF_table, "w") as w:
        w.write("id,SVF(10^-2)\n")
        w.write("\n".join(w_str_list))


def main():
    in_3D_building = arcpy.GetParameterAsText(0)
    in_3D_points = arcpy.GetParameterAsText(1)
    out_path = arcpy.GetParameterAsText(2)

    if not path.exists(out_path):
        makedirs(out_path)

    out_SVF_table = "/".join([out_path, "SVF.csv"])

    temp_skyline_path = "tempSkylines"
    if not path.exists(temp_skyline_path):
        makedirs(temp_skyline_path)
    
    SVF_dict = GetPointsSVF(in_3D_building, in_3D_points, temp_skyline_path)
    write_SVF_table(SVF_dict, out_SVF_table)
    
    rmdir(temp_skyline_path)
    print("finish")


if __name__ == '__main__':
    main()