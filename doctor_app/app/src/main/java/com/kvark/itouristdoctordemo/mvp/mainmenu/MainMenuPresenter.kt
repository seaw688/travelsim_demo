package com.kvark.itouristdoctordemo.mvp.mainmenu

import android.os.Bundle
import androidx.fragment.app.Fragment
import javax.inject.Inject

class MainMenuPresenter @Inject constructor(
    private var mView: MainMenuView?,
    private val mInteractor: MainMenuInteractor
) : BasePresenter(mView) {

    override fun onViewCreated() {
        super.onViewCreated()
        mView?.initToolbar()
        mView?.addMenuIndicator()
        mView?.setAdapter(mInteractor.getMainMenuItems())
    }

    override fun onViewResumed() {
        super.onViewResumed()
        mView?.notifyMenuIndicatorUpdate()
        mView?.getMainMenuAvailabilityCallback()?.onMainMenuResumed()
        mView?.initToolbar()
    }

    fun onMenuItemClicked(fragmentClass: Class<out Fragment>?, isActive: Boolean) {
        if (isActive) {
            fragmentClass?.let { mView?.replaceFragment(it, mView?.getContainerId() ?: return, Bundle()) }
        }
    }

    override fun onViewStopped() {
        super.onViewStopped()
        mView?.getMainMenuAvailabilityCallback()?.onMainMenuStopped()
    }

    override fun onViewDestroyed() {
        mView = null
    }

    fun updateItemIndicator(item: MainMenuEnum, notifNumber: Int) {
        mView?.setMenuItemIndicator(item, notifNumber)
    }
}