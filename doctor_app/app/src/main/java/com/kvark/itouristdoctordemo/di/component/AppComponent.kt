package com.kvark.itouristdoctordemo.di.component

import android.app.Application
import dagger.Component
import javax.inject.Singleton

@Component(modules = [AppModule::class])
@Singleton
interface AppComponent {
    fun inject(app: Application)

    fun plusSplashScreenActivity(activity: SplashScreenActivity)

    fun plusAuthActivity(activity: AuthActivity)

    fun plusMainActivity(module: MainActivityModule): MainActivityComponent

    fun plusSignInFragment(module: SignInFragmentModule): SignInFragmentComponent

    fun plusSignUpFragment(module: SignUpFragmentModule): SignUpFragmentComponent

    fun plusMainMenuFragment(module: MainMenuFragmentModule): MainMenuFragmentComponent

    fun plusIncomingCallFragment(module: IncomingCallFragmentModule): IncomingCallFragmentComponent

    fun plusPhoneCallService(module: PhoneCallServiceModule): PhoneCallServiceComponent
}