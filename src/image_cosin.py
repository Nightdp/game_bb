from PIL import Image
from numpy import average, linalg, dot


# 余弦相似度


def get_thumbnail(image, size=(81, 35), gray=False):
    image = image.resize(size, Image.ANTIALIAS)
    if gray:
        image = image.convert('L')
    return image


def image_similarity_vectors_via_numpy(image1, image2):
    image1 = get_thumbnail(image1)
    image2 = get_thumbnail(image2)
    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    res = dot(a / a_norm, b / b_norm)
    return res


# 计算相似度
def calc_image_similarity(image_l, image_r):
    return image_similarity_vectors_via_numpy(image_l, image_r)
