def writeFrameToYUVFile(f, frame):
    for h in range(frame.shape[0]):
        for w in range(frame.shape[1]):
            f.write(frame[h, w])