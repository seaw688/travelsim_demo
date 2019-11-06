package com.kvark.itouristdoctordemo.entity

import com.google.gson.annotations.SerializedName

data class User(
    val role: UserRole,
    val email: String,
    @SerializedName("first_login")
    val firstLogin: Boolean,
    var profile: Profile?,
    @SerializedName("first_name")
    val firstName: String,
    @SerializedName("last_name")
    val lastName: String,
    val id: Int,
    var token: String
) {

    enum class UserRole {
        @SerializedName("CUSTOMER")
        CUSTOMER,
        @SerializedName("DOCTOR")
        DOCTOR
    }
}