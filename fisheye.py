# -*- coding: utf-8 -*-
import cv2
import numpy as np  
import math


# // map the fisheye image position to the rectilinear image position
# // input:  src_x, src_y, center_x, center_y, R,
# // output: dst_x, dst_y
def rectxy2fisheyexy( src_x,  src_y,  center_x,  center_y, image_width, R):
    D = math.sqrt( R * R - image_width*image_width/4)
    src_x -= center_x
    src_y -= center_y
    phi = math.atan( math.sqrt( (src_x*src_x+src_y*src_y))/ D )
    theta = math.atan2(src_y, src_x)
    dst_x = R * math.sin(phi) * math.cos(theta) + center_x
    dst_y = R * math.sin(phi) * math.sin(theta) + center_y
    return dst_x, dst_y



def rectify(img, center=None, raidus=None):
    imgh = img.shape[0]
    imgw = img.shape[1]
    out_h = int(imgh*1.25)
    out_w = int(imgw*1.25)

    fisheye_radius = 1500 #you can adjust the parameter in range [1500, +INF]
    wrapped_img = 255 * np.ones((out_h, out_w, 3), dtype="u1")
    for r in range(out_h):
        for c in range(out_w):
            src_c, src_r  = rectxy2fisheyexy(c-(out_w-imgw)/2 , r-(out_h-imgw)/2, imgw/2.0, imgh/2.0, imgw, fisheye_radius)
            src_c, src_r = round(src_c) ,round(src_r)
            # print(src_c, src_r)
            # copy the current pixel if it's in the range
            if src_r > 0 and src_r < imgh-1 and src_c > 0 and src_c < imgw-1:
                wrapped_img[r, c, :] = img[src_r, src_c, :]
    return wrapped_img



if __name__ ==  "__main__":
    img_path = r"D:\fisheye\mars.jpg"
    src  = cv2.imread(img_path)
    dst = rectify(src)
    cv2.imwrite(r"D:\fisheye\mars-rectify.jpg", dst)