package com.kvark.itouristdoctordemo.di.module

import android.content.Context
import dagger.Module
import dagger.Provides
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory
import retrofit2.converter.gson.GsonConverterFactory
import javax.inject.Singleton

@Module
class ApiNetworkModule {

    @Singleton
    @Provides
    fun provideOkHttpClient(
        requestHeadersInterceptor: RequestHeadersInterceptor,
        netConnectionInterceptor: NetworkConnectionInterceptor,
        responseInterceptor: ResponseInterceptor
    ): OkHttpClient = OkHttpClient.Builder()
        .addInterceptor(requestHeadersInterceptor)
        .addInterceptor(netConnectionInterceptor)
        .addInterceptor(responseInterceptor)
        .build()

    @Singleton
    @Provides
    fun provideNetworkConnectionInterceptor(networkConnectionVerifier: NetworkConnectionVerifier) =
        NetworkConnectionInterceptor(networkConnectionVerifier)

    @Singleton
    @Provides
    fun provideRetrofitBuilder(okHttpClient: OkHttpClient): Retrofit.Builder = retrofit2.Retrofit.Builder()
        .client(okHttpClient)
        .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
        .addConverterFactory(GsonConverterFactory.create())

    @Singleton
    @Provides
    fun provideApiService(retrofit: Retrofit.Builder): ApiService =
        retrofit.baseUrl(API_URL).build().create(ApiService::class.java)

    @Singleton
    @Provides
    fun provideNetworkConnectionVerifier(context: Context) = NetworkConnectionVerifier(context)
}