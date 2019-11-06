package com.kvark.itouristdoctordemo.mvp.mainmenu

interface MainMenuView : BaseFragmentView {
    fun setMainMenuAvailabilityCallback(callback: MainMenuAvailabilityCallback)

    fun getMainMenuAvailabilityCallback(): MainMenuAvailabilityCallback?

    fun openNavigationDrawer()

    fun setAdapter(list: List<MainMenu>)

    fun addMenuIndicator()

    fun setMenuItemIndicator(item: MainMenuEnum, notifNumber: Int)

    fun notifyMenuIndicatorUpdate()
}