package com.kvark.itouristdoctordemo.mvp.mainmenu

import javax.inject.Inject

class MainMenuInteractor @Inject constructor(private val mResManager: ResourceManager) : BaseInteractor() {

    fun getMainMenuItems(): List<MainMenu> {
        val list = arrayListOf<MainMenu>()
        enumValues<MainMenuEnum>().forEach {
            list.add(
                MainMenu(it.iconId, mResManager.getString(it.titleId), it.fragmentClass, getNotificationCount(it))
            )
        }
        return list
    }
}