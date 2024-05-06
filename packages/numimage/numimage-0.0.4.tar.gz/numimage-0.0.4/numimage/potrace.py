

from PIL import Image,ImageChops
from potrace import Bitmap, POTRACE_TURNPOLICY_MINORITY  
from potrace import Bitmap, POTRACE_TURNPOLICY_MINORITY 

def fileVectorize(filename: str):
    try:
        image = Image.open(filename).convert('L')
        image = ImageChops.invert(image)
    except IOError:
        print("Image (%s) could not be loaded." % filename)
        return
    
    bm = Bitmap(image, blacklevel=0.5)
    # bm.invert()
    plist = bm.trace(
        turdsize=2,
        turnpolicy=POTRACE_TURNPOLICY_MINORITY,
        alphamax=1,
        opticurve=False,
        opttolerance=0.2,
    )
    with open(f"{filename}.svg", "w") as fp:
        fp.write(
            f'''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{image.width*2}" height="{image.height*2}" viewBox="0 0 {image.width*2} {image.height*2}">''')
        fp.write(
            f'''<g transform="scale(1.5)">''')
        parts = []
        for curve in plist:
            fs = curve.start_point
            parts.append(f"M{fs.x},{fs.y}")
            for segment in curve.segments:
                if segment.is_corner:
                    a = segment.c
                    b = segment.end_point
                    parts.append(f"L{a.x},{a.y}L{b.x},{b.y}")
                else:
                    a = segment.c1
                    b = segment.c2
                    c = segment.end_point
                    parts.append(f"C{a.x},{a.y} {b.x},{b.y} {c.x},{c.y}")
            parts.append("z")
        fp.write(f'<path stroke="none" fill="red" fill-rule="evenodd" d="{"".join(parts)}"/>')
        fp.write("</g>")
        fp.write("</svg>")




def imgVectorize(image=None,color:str="#FFF",scalex:float=1.0,scaley:float=1.0,outputformat:str="svg",translatex:float=0,translatey:float=0,rotate:float=0,centerx:float=0,centery:float=0):


    # if len(image.shape) == 2:
    #     logo = image
    # elif image.shape[2] == 3:
    #     _,_,logo = kmeans_rmbg(image)
    # else:
    #     logo = image[:,:,-1]
  

    # logo = Image.fromarray(logo)
    image = image.convert('L')
    logo = ImageChops.invert(image)

    # 转换svg
    bm = Bitmap(logo, blacklevel=0.5)
    # bm.invert()
    plist = bm.trace(
        turdsize=2,
        turnpolicy=POTRACE_TURNPOLICY_MINORITY,
        alphamax=1,
        opticurve=False,
        opttolerance=0.2,
    )

    if outputformat=="svg":
        svgs = ['''<g transform=" rotate({rotate},{centerx},{centery})  translate({x},{y}) scale({scalex},{scaley})">'''.format(x=translatex,y=translatey,scalex=scalex,scaley=scaley,rotate=rotate,centerx=centerx,centery=centery)]
        parts = []
        for curve in plist:
            fs = curve.start_point
            parts.append(f"M{fs.x},{fs.y}")
            for segment in curve.segments:
                if segment.is_corner:
                    a = segment.c
                    b = segment.end_point
                    parts.append(f"L{a.x},{a.y}L{b.x},{b.y}")
                else:
                    a = segment.c1
                    b = segment.c2
                    c = segment.end_point
                    parts.append(f"C{a.x},{a.y} {b.x},{b.y} {c.x},{c.y}")
            parts.append("z")
        svgs.append(f'<path stroke="none" fill="{color}" fill-rule="evenodd" d="{"".join(parts)}"/>'.format(color=color))
        svgs.append('</g>')
        return svgs
   