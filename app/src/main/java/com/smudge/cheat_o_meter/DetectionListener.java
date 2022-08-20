package com.smudge.cheat_o_meter;

import org.opencv.core.Rect;

public interface DetectionListener {
    void FaceDetected(Rect rect, double adjx, double adjy);
    void EyesDetected(Rect facerect, Rect eyesrect);

}
