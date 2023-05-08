# IMAGE PROCESSING
from PIL import Image
import numpy as np
import pandas as pd
import extcolors
from colormap import rgb2hex
from sklearn.cluster import KMeans


# rgb to hex function
def rgb_to_hex(rgb_input):

    rgb_list = rgb_input[0]
    occurrence_list = rgb_input[1]
    # convert RGB to HEX code
    hex_colors = [rgb2hex(int(i[0]), int(i[1]), int(i[2])) for i in rgb_list]

    df = pd.DataFrame(zip(hex_colors, occurrence_list), columns=['c_code', 'occurrence'])
    df['occurrence'] = round(df['occurrence'], 8)
    color_dict = df.to_dict(orient='records')
    return color_dict


def extract_colors(input_img='static/demo-img.jpg', num_of_col=10, tolerance=12):

    #resizing image for faster processing
    output_width = 900
    img = Image.open(input_img)

    output_height = int((float(img.size[1] * float(output_width / float(img.size[0])))))
    img = img.resize((output_width, output_height), Image.ANTIALIAS)
    img_array = np.array(img)

    #reshaping image for 2 dimesnsion to work with KMeans
    clt_img = img_array.reshape((img_array.shape[0]*img_array.shape[1], img_array.shape[2]))
    clt_img_list = clt_img.tolist()

    cluster = KMeans(n_clusters=num_of_col, tol=tolerance)
    cluster.fit(clt_img)

    colors = [i.astype('uint8').tolist() for i in cluster.cluster_centers_]

    labels = np.arange(0, len(np.unique(cluster.labels_))+1)
    (hist, _) = np.histogram(cluster.labels_, bins=labels)
    hist = hist.astype('float')

    #getting occurency proportion
    hist /= hist.sum()
    hist = hist.tolist()
    rgb_in = (colors, hist)

    #calling rgb to hex function
    df_color = rgb_to_hex(rgb_in)
    return df_color


