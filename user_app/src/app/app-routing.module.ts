import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from 'src/app/guards/auth.guard';
import { GuestGuard } from 'src/app/guards/guest.guard';
import { NetworkGuard } from 'src/app/guards/network.guard';
import { MedicalHistoryGuard } from 'src/app/guards/medical-history.guard';
import { FirstStartGuard } from 'src/app/guards/first-start.guard';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'onboarding-tour',
    pathMatch: 'full'
  },
  {
    path: 'choose-company',
    loadChildren: './pages/customer/choose-company/choose-company.module#ChooseCompanyPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'choose-plan/:companyId',
    loadChildren: './pages/customer/choose-plan/choose-plan.module#ChoosePlanPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'confirm-plan/:companyId/:planId',
    loadChildren: './pages/customer/confirm-plan/confirm-plan.module#ConfirmPlanPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'my-plan',
    loadChildren: './pages/customer/my-plan/my-plan.module#MyPlanPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'main',
    loadChildren: './pages/customer/main/main.module#MainPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'profile-start',
    loadChildren: './pages/customer/profile-start/profile-start.module#ProfileStartPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'profile',
    loadChildren: './pages/customer/profile/profile.module#ProfilePageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'my-requests',
    loadChildren: './pages/customer/my-requests/my-requests.module#MyRequestsPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'alerts-and-notifications',
    loadChildren: './pages/customer/alerts-and-notifications/alerts-and-notifications.module#AlertsAndNotificationsPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'sim-card-start',
    loadChildren: './pages/customer/sim-card-start/sim-card-start.module#SimCardStartPageModule',
    canActivate: [NetworkGuard]
  },
  // {
  //   path: 'enter-mobile-number/:companyId/:planId',
  //   loadChildren: './pages/customer/enter-mobile-number/enter-mobile-number.module#EnterMobileNumberPageModule',
  //   canActivate: [AuthGuard, NetworkGuard]
  // },
  {
    path: 'enter-mobile-number',
    loadChildren: './pages/customer/enter-mobile-number/enter-mobile-number.module#EnterMobileNumberPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'online-doctor-start',
    loadChildren: './pages/customer/online-doctor-start/online-doctor-start.module#OnlineDoctorStartPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'weather-start',
    loadChildren: './pages/customer/weather-start/weather-start.module#WeatherStartPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'weather',
    loadChildren: './pages/customer/weather/weather.module#WeatherPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'online-doctor-choose',
    loadChildren: './pages/customer/online-doctor-choose/online-doctor-choose.module#OnlineDoctorChoosePageModule',
    canActivate: [NetworkGuard, MedicalHistoryGuard]
  },
  {
    path: 'online-doctor-prescriptions',
    loadChildren: './pages/customer/online-doctor-prescriptions/online-doctor-prescriptions.module#OnlineDoctorPrescriptionsPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'online-doctor-calls-list',
    loadChildren: './pages/customer/online-doctor-calls-list/online-doctor-calls-list.module#OnlineDoctorCallsListPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'doctor-appointment',
    loadChildren: './pages/customer/doctor-appointment/doctor-appointment.module#DoctorAppointmentPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'check-up-services',
    loadChildren: './pages/customer/check-up-services/check-up-services.module#CheckUpServicesPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'check-up-disclaimer',
    loadChildren: './pages/customer/check-up-disclaimer/check-up-disclaimer.module#CheckUpDisclaimerPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'check-up-services-start',
    loadChildren: './pages/customer/check-up-services-start/check-up-services-start.module#CheckUpServicesStartPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'qr-code-reader',
    loadChildren: './pages/customer/qr-code-reader/qr-code-reader.module#QrCodeReaderPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'medical-history',
    loadChildren: './pages/customer/medical-history/medical-history.module#MedicalHistoryPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'set-start-info/:userId',
    loadChildren: './pages/customer/set-start-info/set-start-info.module#SetStartInfoPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'calls-packages',
    loadChildren: './pages/customer/calls-packages/calls-packages.module#CallsPackagesPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  },
  {
    path: 'sim-card-choose',
    loadChildren: './pages/customer/sim-card-choose/sim-card-choose.module#SimCardChoosePageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'order-sim-start',
    loadChildren: './pages/customer/order-sim-start/order-sim-start.module#OrderSimStartPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'addresses-list',
    loadChildren: './pages/customer/addresses-list/addresses-list.module#AddressesListPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'order-sim-form',
    loadChildren: './pages/customer/order-sim-form/order-sim-form.module#OrderSimFormPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'alerts-and-notifications-start',
    // tslint:disable-next-line: max-line-length
    loadChildren: './pages/customer/alerts-and-notifications-start/alerts-and-notifications-start.module#AlertsAndNotificationsStartPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'privacy-policy',
    loadChildren: './pages/customer/privacy-policy/privacy-policy.module#PrivacyPolicyPageModule',
    canActivate: [NetworkGuard]
  },
  {
    path: 'register',
    loadChildren: './pages/auth/register/register.module#RegisterPageModule',
    canActivate: [GuestGuard, NetworkGuard]
  },
  {
    path: 'login',
    loadChildren: './pages/auth/login/login.module#LoginPageModule',
    canActivate: [GuestGuard, NetworkGuard]
  },
  {
    path: 'forgot-password',
    loadChildren: './pages/auth/forgot-password/forgot-password.module#ForgotPasswordPageModule',
    canActivate: [GuestGuard, NetworkGuard]
  },
  {
    path: 'onboarding-tour',
    loadChildren: './pages/customer/onboarding-tour/onboarding-tour.module#OnboardingTourPageModule',
    canActivate: [FirstStartGuard, NetworkGuard]
  },
  {
    path: 'choose-credit-card',
    loadChildren: './pages/customer/choose-credit-card/choose-credit-card.module#ChooseCreditCardPageModule',
    canActivate: [AuthGuard, NetworkGuard]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
