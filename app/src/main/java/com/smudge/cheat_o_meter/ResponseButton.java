package com.smudge.cheat_o_meter;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.RectF;
import android.util.AttributeSet;
import android.widget.Button;

import org.opencv.core.Rect;

@SuppressLint("AppCompatCustomView")
public class ResponseButton extends Button {

    private Bitmap buttonimg;
    private Paint white;
    private Paint darkgrey;
    private RectF buttonrect;
    private boolean click;


    public ResponseButton(Context context) {
        super(context);
        init();
    }

    public ResponseButton(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public ResponseButton(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }

    private void init() {
        white = new Paint(Paint.ANTI_ALIAS_FLAG);
        white.setStyle(Paint.Style.FILL);
        white.setColor(getResources().getColor(R.color.white));

        darkgrey = new Paint(Paint.ANTI_ALIAS_FLAG);
        darkgrey.setStyle(Paint.Style.FILL);
        darkgrey.setColor(getResources().getColor(R.color.darkgrey));

        buttonrect = new RectF();
    }

    public void setBImg(int resource) {
        buttonimg = BitmapFactory.decodeResource(getResources(), resource);
        buttonimg = Bitmap.createBitmap(buttonimg);

    }

    @Override
    public void onMeasure(int w, int h) {
        int wt = getResources().getDisplayMetrics().widthPixels;
        int btnwt = wt / 16;

        buttonrect.set(0, 0, btnwt, btnwt);

        setMeasuredDimension(btnwt, btnwt);
    }

    @Override
    public void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        if (click == false) {
                canvas.drawOval(buttonrect, darkgrey);
                canvas.drawBitmap(buttonimg, null, buttonrect, null);
            }
            else {
                canvas.drawOval(buttonrect, white);
                canvas.drawBitmap(buttonimg, null, buttonrect, null);
            }


    }


    public void setClick(boolean isclick) {
        this.click = isclick;
    }
}
