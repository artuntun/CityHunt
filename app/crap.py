#===================================================================================
#
#===================================================================================
if 1:
    ########### Python 3.2 #############
    import http.client, urllib.request, urllib.parse, urllib.error, base64
    import json


#===================================================================================
if 1:
    def get_emotions(image_url=""):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '7cef923318814299bf3efb87d7ba809a',
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'returnFaceId': 'false',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,emotion'
        })

        body = json.dumps({
            "url": image_url
        })

        try:
            conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

            print( "Obtaining response...")
            conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
            response = conn.getresponse()

            data = response.read()
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))


        data = data.decode("utf-8")
        print("Data loaded")
        list_emotions = []
        Npeople = len(json.loads(data))

        for i in range(Npeople):
            data_json = json.loads(data)[i]
            # emotions = data_json["faceAttributes"]["emotion"]
            list_emotions.append(data_json["faceAttributes"]["emotion"])

            # fr = data_json["faceRectangle"]

        return list_emotions



image_url = 'http://bh-s2.azureedge.net/bh-uploads/2016/01/1098_01.jpg'
image_url = 'https://www.costumebox.com.au/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/6/0/60029-guardhat.jpg'
get_emotions(image_url)



#===================================================================================
# Google image annotator
#===================================================================================
if 0:
    from app.ImageAnnotator import ImageAnnotator
    import os

    imm = ImageAnnotator()

    names = os.listdir(os.getcwd() + '/resources')
    test_images = [os.getcwd() + '/resources/' + name for name in names]

    for image in test_images:
        landmarks = imm.get_landmark(image)
        print('\n', image, landmarks)



