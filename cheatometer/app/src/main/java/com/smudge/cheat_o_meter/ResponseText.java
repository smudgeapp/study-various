package com.smudge.cheat_o_meter;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.Rect;
import android.graphics.RectF;
import android.support.annotation.Nullable;
import android.text.Layout;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.RelativeLayout;
import android.widget.TextView;

public class ResponseText extends View {

    private Paint white;
    private Paint darkgrey;
    private RectF textrect;
    private boolean lit = false;


    public ResponseText(Context context) {
        super(context);
        init();
    }

    public ResponseText(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public ResponseText(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }

    private void init() {
        white = new Paint(Paint.ANTI_ALIAS_FLAG);
        white.setStyle(Paint.Style.FILL);
        white.setColor(getResources().getColor(R.color.white));


        darkgrey = new Paint(Paint.ANTI_ALIAS_FLAG);
        darkgrey.setStyle(Paint.Style.STROKE);
        darkgrey.setColor(getResources().getColor(R.color.darkgrey));


        textrect = new RectF();
    }

    @Override
    public void onMeasure(int w, int h) {
        int wt = MeasureSpec.getSize(w);
        int rht = MeasureSpec.getSize(h);
        textrect.set(0, 0, wt, rht);

        setMeasuredDimension(wt, rht);
    }

    @Override
    public void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        Path path = new Path();
        path.addRect(textrect, Path.Direction.CW);

        if (lit == false) {
            canvas.drawRoundRect(textrect, 20, 20, darkgrey);
            }
            else {
            canvas.drawRoundRect(textrect, 20, 20, white);
            }
    }

    public void setLit(boolean light) {

        this.lit = light;
    }
}
