package com.kvark.itouristdoctordemo.mvp

interface BaseView {
    fun setupComponents(appComponent: AppComponent)

    fun clearFragmentsBackStack()
}