package com.kvark.itouristdoctordemo.entity

import android.os.Parcelable
import com.google.gson.annotations.SerializedName
import kotlinx.android.parcel.Parcelize

@Parcelize
data class Patient(
    val id: Int,
    @SerializedName("first_name")
    val firstName: String,
    @SerializedName("last_name")
    val lastName: String,
    @SerializedName("profile")
    val patientProfile: PatientProfile,
    @SerializedName("medical_history")
    val medicalHistories: List<MedicalHistory>
) : Parcelable

@Parcelize
data class PatientProfile(
    @SerializedName("passport_image")
    val passportImg: String?,
    @SerializedName("medical_image")
    val medicalImg: String?,
    @SerializedName("date_birth")
    val dateOfBirth: String?,
    val age: Int?,
    var photo: String?
) : Parcelable