import os
import cv2

dirs = os.listdir('Images')

project = os.path.realpath('')


annotation = open(project + '/Annotations/annotations.txt','w+')
train = open(project + '/Images/train.txt','w+')

annotation_list = []
train_list = []

def isdigit(string):

    try:
        string = int(string)
    except ValueError:
        return False

    return True

def xml(image, cls, coordinate):


    xml = open(os.path.join(project, 'Annotations', cls , image + '.xml'), 'w+')

    xml.write(
        '<annotation>\n'
            ' <folder>dog_cat</folder>\n'
                '  <filename>\n'
                    '   <item>{}</item>\n'
                '  </filename>\n'
                '  <object>\n'
                    '   <name>{}</name>\n'
                    '   <bndbox>\n'
                        '    <xmin>{}</xmin>\n'
                        '    <ymin>{}</ymin>\n'
                        '    <xmax>{}</xmax>\n'
                        '    <ymax>{}</ymax>\n'
                    '   </bndbox>\n'
                '   </object>\n'
        '</annotation>\n'.format(
            image,
            cls,
            coordinate[0],
            coordinate[1],
            coordinate[2],
            coordinate[3])
        )


    xml.close

    return


def arrange(directory):
    cls = directory.split('/')[-1]
    #os.chdir(directory)
    #directory = os.path.join('Images', directory)
    images = os.listdir(directory)
    
    check_exist = 0

    count = 0

    for image in images:

        try:
            name, ext = image.split('.')

            
        except:
            continue

        
        if ext != 'jpg':
            continue 
        try:       # check if name is correct
            check_cls, no = name.split('_')
            
            assert cls == check_cls
            assert isdigit(no) == True 
            

        except:    # rename the image 

            while os.path.isfile(
                os.path.join(
                    directory, '{}_{}'.format(directory, check_exist))):
                check_exist += 1
            print directory
            print name
            abs_name = '{}/{}_{}'.format(directory, cls, check_exist)
            print name
            name = '{}_{}'.format(cls,check_exist)
            print os.path.join(directory,image)
            print os.path.join(directory,name + '.jpg')

            os.rename(os.path.join(directory,image),
                os.path.join(directory, name + '.jpg'))

 
        image = cv2.imread(os.path.join(directory, name + '.jpg'))

        
        height, width =  image.shape[:-1]



        annotations = '{}/{} {} {} {} {} {}\n'.format(
            cls, 
            name + '.jpg',
            cls,
            0, 0, width, height)

        
        #annotation.writelines(annotations)

        coordinate = [0, 0, width, height]

        xml(name, cls, coordinate)

        train.writelines('{}/{}\n'.format(cls,name))

        count += 1


    return count






    
    
            


for item in dirs:

    abs_path = os.path.join('Images', item)
    
    if os.path.isdir(abs_path):        
        numbers = arrange(abs_path)
        print '{} --> {}'.format(item, numbers) 
    else:
        pass





annotation.close()
train.close()
print 'done'