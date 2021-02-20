final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
      if iswebp:
          final_transparent_image.thumbnail((512,512))
      final_transparent_image.save(file)
  else:
      inverted_image = PIL.ImageOps.invert(image)
      if iswebp:
          inverted_image.thumbnail((512,512))
      inverted_image.save(file)
  file.seek(0)
  return file
async def contrast(im, level, ext):
  image = ImageEnhance.Contrast(Image.open(im)).enhance(level)
  out = io.BytesIO()
  iswebp = True if ext == ".webp" else False
  if iswebp:
    image.thumbnail((512,512))
  out.name = "contrast." + (".webp" if iswebp else ".png")
  image.save(out)
  out.seek(0)
  return out
async def blwh(im, ext):
  image = Image.open(im).convert('L')
  out = io.BytesIO()
  iswebp = True if ext == ".webp" else False
  if iswebp:
    image.thumbnail((512,512))
  out.name = "bw." + (".webp" if iswebp else ".png")
  image.save(out)
  out.seek(0)
  return out
def setbright(im, level, ext):
    iswebp = True if ext == ".webp" else False
    image = ImageEnhance.Brightness(Image.open(im)).enhance(level)
    if iswebp:
        image.thumbnail((512,512))
    out = io.BytesIO()
    out.name = "brigth." + (".webp" if iswebp else ".png")
    image.save(out)
    out.seek(0)
    return out
def setsharpness(im, level, ext):
    iswebp = True if ext == ".webp" else False
    image = ImageEnhance.Sharpness(Image.open(im)).enhance(level)
    if iswebp:
        image.thumbnail((512,512))
    out = io.BytesIO()
    out.name = "sharpness." + (".webp" if iswebp else ".png")
    image.save(out)
    out.seek(0)
    return out