import io
import os
import mysql.connector
from google.cloud import videointelligence
import sys
import wget
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ggcredentials.json'

# [START video_detect_logo]

def detect_logo(url):
    """Performs asynchronous video annotation for logo recognition on a local file."""
    client = videointelligence.VideoIntelligenceServiceClient()

    filename = wget.download(url)
    with io.open(filename, "rb") as f:
        input_content = f.read()
    features = [videointelligence.Feature.LOGO_RECOGNITION]

    operation = client.annotate_video(
        request={"features": features, "input_content": input_content}
    )

    print(u"Waiting for operation to complete...")
    response = operation.result()

    # Get the first response, since we sent only one video.
    annotation_result = response.annotation_results[0]

    # Annotations for list of logos detected, tracked and recognized in video.
    for logo_recognition_annotation in annotation_result.logo_recognition_annotations:
        entity = logo_recognition_annotation.entity
        brand = entity.description

        # Opaque entity ID. Some IDs may be available in [Google Knowledge Graph
        # Search API](https://developers.google.com/knowledge-graph/).
        print(u"Entity Id : {}".format(entity.entity_id))

        print(u"Description : {}".format(entity.description))

        # All logo tracks where the recognized logo appears. Each track corresponds
        # to one logo instance appearing in consecutive frames.
        for track in logo_recognition_annotation.tracks:
            # Video segment of a track.
            print(
                u"\n\tStart Time Offset : {}.{}".format(
                    track.segment.start_time_offset.seconds,
                    track.segment.start_time_offset.microseconds * 1000,
                )
            )
            print(
                u"\tEnd Time Offset : {}.{}".format(
                    track.segment.end_time_offset.seconds,
                    track.segment.end_time_offset.microseconds * 1000,
                )
            )
            print(u"\tConfidence : {}".format(track.confidence))

            # The object with timestamp and attributes per frame in the track.
            for timestamped_object in track.timestamped_objects:

                # Normalized Bounding box in a frame, where the object is located.
                normalized_bounding_box = timestamped_object.normalized_bounding_box
                print(u"\n\t\tLeft : {}".format(normalized_bounding_box.left))
                print(u"\t\tTop : {}".format(normalized_bounding_box.top))
                print(u"\t\tRight : {}".format(normalized_bounding_box.right))
                print(u"\t\tBottom : {}".format(normalized_bounding_box.bottom))

                # Optional. The attributes of the object in the bounding box.
                for attribute in timestamped_object.attributes:
                    print(u"\n\t\t\tName : {}".format(attribute.name))
                    print(u"\t\t\tConfidence : {}".format(attribute.confidence))
                    print(u"\t\t\tValue : {}".format(attribute.value))

            # Optional. Attributes in the track level.
            for track_attribute in track.attributes:
                print(u"\n\t\tName : {}".format(track_attribute.name))
                print(u"\t\tConfidence : {}".format(track_attribute.confidence))
                print(u"\t\tValue : {}".format(track_attribute.value))

        # All video segments where the recognized logo appears. There might be
        # multiple instances of the same logo class appearing in one VideoSegment.
        for segment in logo_recognition_annotation.segments:
            print(
                u"\n\tStart Time Offset : {}.{}".format(
                    segment.start_time_offset.seconds,
                    segment.start_time_offset.microseconds * 1000,
                )
            )
            print(
                u"\tEnd Time Offset : {}.{}".format(
                    segment.end_time_offset.seconds,
                    segment.end_time_offset.microseconds * 1000,
                )
            )
    return(brand)

def insert_into_db(url, brand='nike', category='sport'):

    #connexion to db
    cnx = mysql.connector.connect(user='root', database='urls_categories')
    cursor = cnx.cursor()

    #insert into db
    cursor.execute("""INSERT INTO urls_table (url, brand, category) VALUES (%s, %s, %s) """,(url, brand, category))

    #comit and close db connexion
    cnx.commit()
    cursor.close()
    cnx.close()

def check_set_db():

    #connexion to db
    cnx = mysql.connector.connect(user='root', database='urls_categories')
    cursor = cnx.cursor()

    sorted_list = ("SELECT * FROM urls_table ORDER BY id DESC LIMIT 2")
    cursor.execute(sorted_list)
    myresult = cursor.fetchall()

    
    tab = []
    for x in myresult:
        tab.append(x)
        
    displayed_0 = ("UPDATE urls_table SET displayed=0 WHERE id=" + str(tab[0][0]))
    displayed_1 = ("UPDATE urls_table SET displayed=1 WHERE id=" + str(tab[0][0]))


    ret = False
    if tab[0][2] == tab[1][2] or tab[0][3] == tab[1][3]:
        cursor.execute(displayed_0)
    else :
        cursor.execute(displayed_1)
        ret = True
 
    #comit and close db connexion
    cnx.commit()   
    cursor.close()
    cnx.close()
    return ret
    


def main():
    url = sys.argv[1]
    print(url)
    brand = detect_logo(url)
    insert_into_db(url, brand, '')
    return check_set_db()

main()
