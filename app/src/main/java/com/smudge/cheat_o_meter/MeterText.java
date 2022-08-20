package com.smudge.cheat_o_meter;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.Rect;
import android.graphics.RectF;
import android.graphics.Typeface;
import android.support.annotation.Nullable;
import android.util.AttributeSet;
import android.view.View;

public class MeterText extends View {

    private Paint arclight1, arclight2, arclight3, arclight4, arclight5;
    private RectF textrect;
    private boolean showtext = false;
    private float angle;

    public MeterText(Context context) {
        super(context);
        init();
    }

    public MeterText(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    public MeterText(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        init();
    }

    private void init() {
        arclight1 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arclight1.setStyle(Paint.Style.FILL);
        arclight1.setColor(getResources().getColor(R.color.nobullL));
        arclight2 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arclight2.setStyle(Paint.Style.FILL);
        arclight2.setColor(getResources().getColor(R.color.dawgL));
        arclight3 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arclight3.setStyle(Paint.Style.FILL);
        arclight3.setColor(getResources().getColor(R.color.uhohL));
        arclight4 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arclight4.setStyle(Paint.Style.FILL);
        arclight4.setColor(getResources().getColor(R.color.holdhorsesL));
        arclight5 = new Paint(Paint.ANTI_ALIAS_FLAG);
        arclight5.setStyle(Paint.Style.FILL);
        arclight5.setColor(getResources().getColor(R.color.beastL));

        textrect = new RectF();
    }

    @Override
    public void onMeasure(int width, int height) {
        int w = getResources().getDisplayMetrics().widthPixels;

        int textwt = 3 * (w / 4);
        int textht = MeasureSpec.getSize(height);
        textrect.set(0, 0, textwt, textht);
        setMeasuredDimension(textwt, textht);
    }

    @Override
    public void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        Path path = new Path();
        path.addRect(textrect, Path.Direction.CW);

        if (showtext == true) {
            if (-130 < angle && angle <= -78) {
                canvas.drawRoundRect(textrect, 20, 20, arclight1);

            } else if (-78 < angle && angle <= -26) {
                canvas.drawRoundRect(textrect, 20, 20, arclight2);

            } else if (-26 < angle && angle <= 26) {
                canvas.drawRoundRect(textrect, 20, 20, arclight3);

            } else if (26 < angle && angle <= 78) {
                canvas.drawRoundRect(textrect, 20, 20, arclight4);

            } else if (78 < angle && angle <= 130) {
                canvas.drawRoundRect(textrect, 20, 20, arclight5);

            }
        }


    }

    public void setText(boolean show, float angle) {
        this.showtext = show;
        this.angle = angle;
    }

}
