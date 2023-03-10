from PIL import Image, ImageDraw
import numpy as np
import csv
import math
from random import *

def ReadKeys(image):
    """Input an image and its associated SIFT keypoints.

    The argument image is the image file name (without an extension).
    The image is read from the PGM format file image.pgm and the
    keypoints are read from the file image.key.

    ReadKeys returns the following 3 arguments:

    image: the image (in PIL 'RGB' format)

    keypoints: K-by-4 array, in which each row has the 4 values specifying
    a keypoint (row, column, scale, orientation).  The orientation
    is in the range [-PI, PI] radians.

    descriptors: a K-by-128 array, where each row gives a descriptor
    for one of the K keypoints.  The descriptor is a 1D array of 128
    values with unit length.
    """
    im = Image.open(image+'.pgm').convert('RGB')
    keypoints = []
    descriptors = []
    first = True
    with open(image+'.key','r') as f:
        reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC,skipinitialspace = True)
        descriptor = []
        for row in reader:
            if len(row) == 2:
                assert first, "Invalid keypoint file header."
                assert row[1] == 128, "Invalid keypoint descriptor length in header (should be 128)."
                count = row[0]
                first = False
            if len(row) == 4:
                keypoints.append(np.array(row))
            if len(row) == 20:
                descriptor += row
            if len(row) == 8:
                descriptor += row
                assert len(descriptor) == 128, "Keypoint descriptor length invalid (should be 128)."
                #normalize the key to unit length
                descriptor = np.array(descriptor)
                descriptor = descriptor / math.sqrt(np.sum(np.power(descriptor,2)))
                descriptors.append(descriptor)
                descriptor = []
    assert len(keypoints) == count, "Incorrect total number of keypoints read."
    print ("Number of keypoints read:", int(count))
    return [im,keypoints,descriptors]

def AppendImages(im1, im2):
    """Create a new image that appends two images side-by-side.

    The arguments, im1 and im2, are PIL images of type RGB
    """
    im1cols, im1rows = im1.size
    im2cols, im2rows = im2.size
    im3 = Image.new('RGB', (im1cols+im2cols, max(im1rows,im2rows)))
    im3.paste(im1,(0,0))
    im3.paste(im2,(im1cols,0))
    return im3

def DisplayMatches(im1, im2, matched_pairs):
    """Display matches on a new image with the two input images placed side by side.

    Arguments:
     im1           1st image (in PIL 'RGB' format)
     im2           2nd image (in PIL 'RGB' format)
     matched_pairs list of matching keypoints, im1 to im2

    Displays and returns a newly created image (in PIL 'RGB' format)
    """
    im3 = AppendImages(im1,im2)
    offset = im1.size[0]
    draw = ImageDraw.Draw(im3)
    for match in matched_pairs:
        draw.line((match[0][1], match[0][0], offset+match[1][1], match[1][0]),fill="red",width=2)
    im3.show()
    return im3

def match(image1,image2):
    """Input two images and their associated SIFT keypoints.
    Display lines connecting the first 5 keypoints from each image.
    Note: These 5 are not correct matches, just randomly chosen points.

    The arguments image1 and image2 are file names without file extensions.

    Returns the number of matches displayed.

    Example: match('scene','book')
    """
    im1, keypoints1, descriptors1 = ReadKeys(image1)
    im2, keypoints2, descriptors2 = ReadKeys(image2)
    #
    # REPLACE THIS CODE WITH YOUR SOLUTION (ASSIGNMENT 5, QUESTION 3)
    #
    #bestmatch = 2 * math.pi
    
    matched_pairs = []
    for r in range(len(descriptors1)):
        matches = []
        #for each vector in descriptor1 create an array to store all angle values with every
        #   vectors in the descriptor2
        for rr in range(len(descriptors2)):
            #calculate the samility with each pair of vectors
            match = math.acos(np.dot(descriptors1[r],descriptors2[rr]))
            matches.append(match)
        #find the best match best1 with smallest angle value
        #   and the second best match best2
        best1 = sorted(matches)[0]
        best2 = sorted(matches)[1]
        #find the index of best1
        i1 = matches.index(best1)
        #find the ratio for culling
        ratio = best1/best2
        threshold = 0.82
        # import pdb; pdb.set_trace()
        if(ratio < threshold):
            #add them to matched_pairs once it smaller than the threhold
            matched_pairs.append([keypoints1[r],keypoints2[i1]])
    #randomlist contains 10 randomly chosen elements form match_pairs
    randomlist = sample(matched_pairs, 10)
    #consistencSets stores each consistency set for each chosen matched_pairs
    #CSsize stores the size of those consistency sets
    consistencSets = []
    CSsize = []

    for rp in randomlist:
        consistency = []
        for pairs in matched_pairs:
            #calculate the difference and ratio between each pair 
            rp1 = rp[0]
            rp2 = rp[1]
            p1 = pairs[0]
            p2 = pairs[1]
            A1 = rp1[0] -p1[0]
            A2 = rp2[0]- p2[0]
            S1 = (rp1[1] -p1[1])/rp1[1]
            S2 = (rp2[1]- p2[1])/rp2[1]
            Orthrehold = math.pi/8
            Sclethrehold = 0.4
            if(A1< Orthrehold and A1< Orthrehold and abs(S1)<Sclethrehold and abs(S2)<Sclethrehold):
                #if satisfy all requirement add that vector to the consistency set of current vector
                consistency.append(pairs)
            #add each consistency set and its size to coresponding list
            consistencSets.append(consistency)
            CSsize.append(len(consistency))
    #find the maximun one
    maxone = max(CSsize)
    maxIndex = CSsize.index(maxone)
    #set the matched_pairs to the max one
    matched_pairs = consistencSets[maxIndex]







    #Generate five random matches (for testing purposes)
    #matched_pairs = []
    #num = 5
    #for i in range(num):
        #matched_pairs.append([keypoints1[i],keypoints2[i]])
    #
    # END OF SECTION OF CODE TO REPLACE
    #
    im3 = DisplayMatches(im1, im2, matched_pairs)
    return im3

#Test run...
match('library','library2')

