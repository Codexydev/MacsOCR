     if image.getpixel((i,int(middle_y))) == (0,0,0) and image.getpixel((i+1,int(middle_y))) == (0,0,0) :
                    x_intersect+=1
                if image.getpixel((int(middle_x),j)) == (0,0,0) and image.getpixel((int(middle_y),j+1)) == (0,0,0):
                    y_intersect +=1