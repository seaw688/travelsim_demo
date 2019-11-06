package com.kvark.itouristdoctordemo.extensions

import android.content.Context
import android.graphics.PorterDuff
import android.view.LayoutInflater
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.EditText
import android.widget.ImageView
import androidx.appcompat.widget.SearchView
import androidx.appcompat.widget.Toolbar
import io.reactivex.Observable
import io.reactivex.ObservableOnSubscribe
import io.reactivex.android.schedulers.AndroidSchedulers
import io.reactivex.disposables.Disposable
import java.util.concurrent.TimeUnit

fun Context.inflateView(layoutId: Int): View =
    (getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater).inflate(layoutId, null)

fun Context.getInflater() = getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater

fun EditText.setActionDoneListener(onActionDone: () -> Unit) {
    setOnEditorActionListener { _, actionId, _ ->
        if (actionId == EditorInfo.IME_ACTION_DONE) {
            onActionDone()
        }
        false
    }
}

fun View.setVisibilityIfAnother(newVisibility: Int) {
    if (visibility != newVisibility) {
        visibility = newVisibility
    }
}

fun View.showWithAnim(animDuration: Long) {
    alpha = 0f
    visibility = View.VISIBLE
    this.animate()
        .alpha(1f)
        .setDuration(animDuration)
        .setListener(null)
}

fun ImageView.changeIconColor(color: Int) {
    setColorFilter(color, PorterDuff.Mode.SRC_ATOP)
}


fun Toolbar.setNavDrawerIcon(navDrawerFragment: NavigationDrawerFragment) {
    navigationIcon = context.resources.getDrawable(R.drawable.ic_nav_drawer)
    setNavigationOnClickListener {
        navDrawerFragment.mPresenter.onOpenNavigationDrawerClicked()
    }
}

fun Toolbar.clearNavIcon() {
    navigationIcon = null
    removeCallbacks {}
}

fun SearchView.clearText() {
    setQuery("", false)
}

fun SearchView.initAsyncTextChangeHandling(callback: OnTextChangedCallback): Disposable {
    return Observable.create(ObservableOnSubscribe<String> { subscriber ->
        setOnQueryTextListener(object : SearchView.OnQueryTextListener {
            override fun onQueryTextSubmit(query: String?): Boolean {
                query?.let { subscriber.onNext(it) }
                return false
            }

            override fun onQueryTextChange(newText: String?): Boolean {
                newText?.let { subscriber.onNext(it) }
                return false
            }
        })
    })
        .map { it.toLowerCase().trim() }
        .debounce(250, TimeUnit.MILLISECONDS)
        .observeOn(AndroidSchedulers.mainThread())
        .subscribe { callback.onTextChanged(it) }
}