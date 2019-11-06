package com.kvark.itouristdoctordemo.util

import android.content.Context
import android.media.MediaPlayer
import android.provider.Settings
import java.io.FileNotFoundException
import javax.inject.Inject

class AudioManager @Inject constructor(private val mContext: Context) {

    private var mediaPlayer: MediaPlayer? = null

    fun playDefaultAudio() {
        try {
            mediaPlayer = MediaPlayer.create(mContext, Settings.System.DEFAULT_RINGTONE_URI)
        } catch (e: FileNotFoundException) {
            e.printStackTrace()
        }
        mediaPlayer?.isLooping = true
        mediaPlayer?.start()
    }

    fun stopPlaying() {
        mediaPlayer?.stop()
    }
}