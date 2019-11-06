package com.kvark.itouristdoctordemo.util

import android.content.Context
import android.graphics.drawable.Drawable

class ResourceManager(private var mContext: Context) {

    fun getString(resourceId: Int): String = mContext.getString(resourceId)

    fun getDrawable(resourceId: Int): Drawable = mContext.getDrawable(resourceId)

    fun getColor(resourceId: Int): Int = mContext.resources.getColor(resourceId)

    fun getUnknownError(): String = mContext.getString(R.string.unknown_error)
}