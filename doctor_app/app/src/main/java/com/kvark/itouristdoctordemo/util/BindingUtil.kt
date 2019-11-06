package com.kvark.itouristdoctordemo.util

import android.graphics.Typeface
import android.os.Handler
import android.text.Spannable
import android.text.SpannableStringBuilder
import android.text.style.StyleSpan
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import androidx.databinding.BindingAdapter
import com.squareup.picasso.Picasso

@BindingAdapter("imageSrc")
fun setImageSrc(imageView: ImageView, imgId: Int) {
    imageView.setImageResource(imgId)
}

@BindingAdapter("imageUrl")
fun loadImage(view: ImageView, imageUrl: String?) {
    var url = imageUrl
    url?.let {
        if (!it.startsWith("http") && !it.startsWith("https")) {
            url = "file://$it"
        }
        Picasso.get().load(url).into(view)
    }
}

@BindingAdapter("boldText", "allText", requireAll = false)
fun setBoldText(view: TextView, boldText: String?, allText: String?) {
    if (boldText == null || boldText.isEmpty()) {
        return
    }
    Handler().post {
        val baseText = allText ?: view.text

        try {
            val str = SpannableStringBuilder(baseText)
            val textPosition = baseText?.indexOf(boldText)
            str.setSpan(
                StyleSpan(Typeface.BOLD),
                textPosition!!, textPosition + boldText.length, Spannable.SPAN_EXCLUSIVE_EXCLUSIVE
            )
            view.text = str
        } catch (e: IndexOutOfBoundsException) {
            e.printStackTrace()
        }
    }
}

@BindingAdapter("alphaEnabled")
fun setAlphaEnabled(view: View, alphaEnabled: Boolean) {
    view.alpha = if (alphaEnabled) 1f else 0.5f
}