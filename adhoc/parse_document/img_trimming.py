from PIL import Image

img = Image.open("/home/tk/sodashi/northernfarm/adhoc/parse_document/data/Amazon Web Servicesネットワーク入門 impress top gearシリーズ /cover.png")

img_crop = img.crop((100,100,1060,1330))
img_crop.save("./test.png" )