package com.smudge.cheat_o_meter;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RectF;
import android.text.method.Touch;
import android.util.AttributeSet;
import android.util.Log;
import android.view.MotionEvent;
import android.widget.Button;

import org.opencv.core.Rect;

@SuppressLint("AppCompatCustomView")
public class ControlButton extends Button {

private RectF buttonrect;
private Paint blwhite;
private Paint black;
private Bitmap buttonimg;
private boolean touch = false;

    public ControlButton(Context context) {
        super(context);
        init();
    }

    public ControlButton(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public ControlButton(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }

    public void setImage(int resource) {
        buttonimg = BitmapFactory.decodeResource(getResources(), resource);
        buttonimg = Bitmap.createBitmap(buttonimg);
    }

    private void init() {
        buttonrect = new RectF();

        black = new Paint(Paint.ANTI_ALIAS_FLAG);
        black.setStyle(Paint.Style.FILL);
        black.setColor(getResources().getColor(R.color.black));


        blwhite = new Paint(Paint.ANTI_ALIAS_FLAG);
        blwhite.setStyle(Paint.Style.FILL);
        blwhite.setColor(getResources().getColor(R.color.white));
 }

    @Override
    public void onMeasure(int w, int h) {
        w = getResources().getDisplayMetrics().widthPixels;
        int dim = w / 12;

        buttonrect.set(0, 0, dim, dim);
        setMeasuredDimension(dim, dim);
    }


    @Override
    public void onDraw(Canvas canvas) {
        super.onDraw(canvas);

      if (touch == true) {
                canvas.drawOval(buttonrect, blwhite);
                canvas.drawBitmap(buttonimg, null, buttonrect, null);
            }
            else {
                canvas.drawOval(buttonrect, black);
                canvas.drawBitmap(buttonimg, null, buttonrect, null);
            }

    }

    public void setTouch(Boolean touch) {
        this.touch = touch;
    }

    public boolean checkTouch() {
        if (touch == true) {
            return true;
        }
        else {
            return false;
        }
    }

}