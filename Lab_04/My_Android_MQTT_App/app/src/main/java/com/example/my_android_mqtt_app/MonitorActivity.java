package com.example.my_android_mqtt_app;

import android.annotation.SuppressLint;
import android.graphics.Color;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;


import com.google.android.material.card.MaterialCardView;
import com.google.android.material.slider.LabelFormatter;
import com.google.android.material.slider.Slider;
import com.google.android.material.switchmaterial.SwitchMaterial;

public class MonitorActivity extends AppCompatActivity {

    @SuppressLint("ClickableViewAccessibility")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_monitor);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main_monitor), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });





        SwitchMaterial mySwitch = findViewById(R.id.SwitchLED);
        TextView TextPower = findViewById(R.id.TextPowerLED);
        ImageView imgLED = findViewById(R.id.imageLED);
        TextView TitleLed = findViewById(R.id.TitleLED);
        imgLED.setColorFilter(getColor(R.color.default500));
        mySwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                // isChecked will be true if the switch is checked, false otherwise
                if (isChecked) {
                    TextPower.setTextColor(getColor(R.color.ledyellow2));
                    TitleLed.setTextColor(getColor(R.color.ledyellow2));
                    imgLED.setColorFilter(getColor(R.color.ledyellow2));
                    imgLED.setElevation(50);
                    //ledCard.setCardBackgroundColor(getColor(R.color.amber));
                } else {
                    //ledCard.setCardBackgroundColor(getColor(com.google.android.material.R.color.m3_sys_color_dynamic_light_surface_container_low ));
                    TextPower.setTextColor(getColor(R.color.default500));
                    TitleLed.setTextColor(getColor(R.color.default500));
                    imgLED.setColorFilter(getColor(R.color.default500));
                    imgLED.setElevation(0);

                }
            }
        });





        SwitchMaterial heaterSw = findViewById(R.id.SwitchHeater);
        ImageView imgHeater = findViewById(R.id.imageHeater);
        TextView TitleHeater = findViewById(R.id.TitleHeater);
        imgHeater.setColorFilter(getColor(R.color.default500));
        heaterSw.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                // isChecked will be true if the switch is checked, false otherwise
                if (isChecked) {
                    TitleHeater.setTextColor(getColor(R.color.heater_red));
                    imgHeater.setColorFilter(getColor(R.color.heater_red));
                    imgHeater.setElevation(50);
                    //ledCard.setCardBackgroundColor(getColor(R.color.amber));
                } else {
                    //ledCard.setCardBackgroundColor(getColor(com.google.android.material.R.color.m3_sys_color_dynamic_light_surface_container_low ));
                    TitleHeater.setTextColor(getColor(R.color.default500));
                    imgHeater.setColorFilter(getColor(R.color.default500));
                    imgHeater.setElevation(0);
                }
            }
        });





        Slider sliderAir = findViewById(R.id.SliderAir);
        ImageView imgAir = findViewById(R.id.air_condition_img);
        TextView titleAir = findViewById(R.id.TitleAirCon);
        imgAir.setColorFilter(getColor(R.color.bright_blue));



        sliderAir.addOnSliderTouchListener(new Slider.OnSliderTouchListener() {
            @Override
            public void onStartTrackingTouch(@NonNull Slider slider) {
                titleAir.setShadowLayer(10, 0, 0, getColor(R.color.cyan));
                imgAir.setElevation(50);
                imgAir.setOutlineAmbientShadowColor(getColor(R.color.cyan));
            }

            @Override
            public void onStopTrackingTouch(@NonNull Slider slider) {
                titleAir.setShadowLayer(0, 0, 0, getColor(R.color.cyan));
            }
        });


//        sliderAir.setOnTouchListener(new View.OnTouchListener() {
//            @Override
//            public boolean onTouch(View v, MotionEvent event) {
//
//
//                //titleAir.setShadowLayer(10, 0, 0, getColor(R.color.cyan));
//
//
////                if (event.getAction() == MotionEvent.ACTION_UP) {// Handle touch up event
////                    titleAir.setShadowLayer(0, 0, 0, getColor(R.color.cyan));
////                    imgAir.setElevation(0);
////                    imgAir.setOutlineAmbientShadowColor(getColor(R.color.cyan));
////                }
////                else {
////
////                }
////                // Return true to indicate that the event has been consumed
//                return true;
//
//            }
//        });









    }

    //



}