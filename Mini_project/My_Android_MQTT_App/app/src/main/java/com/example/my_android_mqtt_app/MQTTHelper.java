package com.example.my_android_mqtt_app;

import android.annotation.SuppressLint;
import android.content.Context;
import android.os.Build;
import android.util.Log;
import android.widget.Toast;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.DisconnectedBufferOptions;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.StandardCharsets;


public class MQTTHelper   {

    public static MQTTHelper myStaticMQTT = null;

    public MqttAndroidClient mqttAndroidClient;

    public final String[] arrayTopics = {"jackwr/feeds/air-conditioner", "jackwr/feeds/water-heater", "jackwr/feeds/led",
            "jackwr/feeds/temp", "jackwr/feeds/humi", "jackwr/feeds/battery"
    };

    final String clientId = "AndroidIoT";
    final String username = "jackwr";
    String password = "aio_jpkR25QWRYQe63DTyOE7EkLcVC";
    final String serverUri = "tcp://io.adafruit.com:1883";
    public boolean inConnected = false;


    public static MQTTHelper GetMQTTClient(Context context){

        if (myStaticMQTT == null){
            myStaticMQTT = new MQTTHelper(context);
            Log.d("TEST", "GET MQTT CLIENT OK");
        }
        else {
            Log.d("TEST", "MQTT CLIENT EXISTED");
        }

        return myStaticMQTT;
    }

    public boolean CheckConnected(){
        return inConnected;
    }

    public MQTTHelper(Context context){
        mqttAndroidClient = new MqttAndroidClient(context, serverUri, clientId);
        Log.d("TEST", "GET MQTT CLIENT CONSTRUCTED");
        mqttAndroidClient.setCallback(new MqttCallbackExtended() {
            @Override
            public synchronized void connectComplete(boolean b, String s) {
                Log.d("CONNECTION", s);
                inConnected = true;
                notify();
                Toast.makeText(context, "MQTT CONNECTED SUCCESSFULLY...", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void connectionLost(Throwable throwable) {
                Toast.makeText(context, "MQTT DISCONNECTING...", Toast.LENGTH_SHORT).show();
                connect();
            }

            @Override
            public void messageArrived(String topic, MqttMessage mqttMessage) throws Exception {
                Log.w("MQTT", mqttMessage.toString());
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {

            }
        });
        connect();

    }

    public void setCallback(MqttCallbackExtended callback) {
        mqttAndroidClient.setCallback(callback);
    }

    public void connect(){
        MqttConnectOptions mqttConnectOptions = new MqttConnectOptions();
        mqttConnectOptions.setAutomaticReconnect(true);
        mqttConnectOptions.setCleanSession(false);
        mqttConnectOptions.setUserName(username);
        password = password + "sh";
        mqttConnectOptions.setPassword(password.toCharArray());

        try {

            mqttAndroidClient.connect(mqttConnectOptions, null, new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {

                    DisconnectedBufferOptions disconnectedBufferOptions = new DisconnectedBufferOptions();
                    disconnectedBufferOptions.setBufferEnabled(true);
                    disconnectedBufferOptions.setBufferSize(100);
                    disconnectedBufferOptions.setPersistBuffer(false);
                    disconnectedBufferOptions.setDeleteOldestMessages(false);
                    mqttAndroidClient.setBufferOpts(disconnectedBufferOptions);
                    subscribeToTopic();
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Log.w("CONNECTION", "Failed to connect to: " + serverUri + exception.toString());
                }
            });


        } catch (MqttException ex){
            ex.printStackTrace();
        }
    }

    private void subscribeToTopic() {
        for (String arrayTopic : arrayTopics) {
            try {
                mqttAndroidClient.subscribe(arrayTopic, 1, null, new IMqttActionListener() {
                    @Override
                    public void onSuccess(IMqttToken asyncActionToken) {
                        Log.d("MQTT", "Subscribed OK!");
                    }

                    @Override
                    public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                        Log.d("MQTT", "Subscribed ERROR!");
                    }
                });

            } catch (MqttException ex) {
                System.err.println("Exceptionst subscribing");
                ex.printStackTrace();
            }
        }
    }



    public void sendDataMQTT(String topic, String value){
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(1);
        msg.setRetained(true);

        byte[] b = value.getBytes(StandardCharsets.UTF_8);
        msg.setPayload(b);

        try {
            myStaticMQTT.mqttAndroidClient.publish(topic, msg);
        } catch (MqttException e) {
            throw new RuntimeException(e);
        }
    }

}