import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { GooglePlus } from '@ionic-native/google-plus/ngx';
import { Facebook } from '@ionic-native/facebook/ngx';

import { of, Observable } from 'rxjs';
import { delay } from 'rxjs/operators';
import * as _ from 'lodash';

import { StorageService } from 'src/app/services/storage.service';

import {
  BaseResponse,
  ProfileEditRequest,
  OrderSimCardRequest,
  // AppointmentRequest,
  CheckupRequest,
  SimPlan,
  RegisterDeviceFcmRequest
} from 'src/app/models/models';

import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    private http: HttpClient,
    private storage: StorageService,
    private googlePlus: GooglePlus,
    private fb: Facebook
  ) { }

  public getCompanies() {
    return this.http.get<BaseResponse>(`${environment.api}/companies`);
  }

  public getPlans(id: string): Observable<any> {
    const httpParams = new HttpParams().set('company_id', id);
    return this.http.get<BaseResponse>(`${environment.api}/simpackages`, { params: httpParams });
  }

  public getPlan(id: string): Observable<BaseResponse> {
    return this.http.get<BaseResponse>(`${environment.api}/simpackages/${id}`);
  }

  public getMyPlan() {
    return this.http.get<BaseResponse>(`${environment.api}/my-simpackages`);
  }

  public register(data: FormData): Observable<BaseResponse> {
    return this.http.post<BaseResponse>(`${environment.api}/registration`, data);
  }

  public sendEmail(email: string) {
    return this.http.post<BaseResponse>(`${environment.api}/password-reset`, { email });
  }

  public postImages(data: any) {
    // const headers = new HttpHeaders().append('Content-Type', 'application/json');
    return this.http.post<BaseResponse>(`${environment.api}/user/profile/photo`, data);
    // return this.http.post<BaseResponse>(`${environment.api}/user/profile/photo`, data, { headers });
  }

  public deleteImages(images: string[]) {
    return this.http.post<BaseResponse>(`${environment.api}/user/profile/photo`, images);
  }

  public googleLogin(data: { id_token: string }): Observable<BaseResponse> {
    return this.http.post<BaseResponse>(`${environment.api}/login-google`, data);
  }

  public facebookLogin(data: { access_token: string, app: string }): Observable<BaseResponse> {
    return this.http.post<BaseResponse>(`${environment.api}/login-facebook`, data);
  }

  public login(data: FormData): Observable<BaseResponse> {
    return this.http.post<BaseResponse>(`${environment.api}/login`, data);
  }

  public logout(): Observable<BaseResponse> {
    return this.http.get<BaseResponse>(`${environment.api}/logout`);
  }

  public async googleLogout() {
    await this.googlePlus.disconnect();
  }

  public async facebookLogout() {
    await this.fb.logout();
  }

  public getToken(): Observable<any> {
    return this.storage.get<any>('token');
  }

  public getProfile(): Observable<BaseResponse> {
    return this.http.get<BaseResponse>(`${environment.api}/user/profile`);
  }

  public editProfile(id: number, user: ProfileEditRequest): Observable<BaseResponse> {
    return this.http.patch<BaseResponse>(`${environment.api}/users/${id}`, user);
  }

  public getHistory(): Observable<BaseResponse> {
    return this.http.get<BaseResponse>(`${environment.api}/action-requests`);
  }

  public getAlerts(): Observable<BaseResponse> {
    return this.http.get<BaseResponse>(`${environment.api}/alerts`);
  }

  public getLatestAlert(): Observable<BaseResponse> {
    const params = new HttpParams().set('earliest', '1');
    return this.http.get<BaseResponse>(`${environment.api}/alerts`, { params });
  }

  public getAddressesList(): Observable<BaseResponse> {
    return this.http.get<BaseResponse>(`${environment.api}/action-requests/pickup-points`);
  }

  public orderSimCard(body: OrderSimCardRequest): Observable<BaseResponse> {
    return this.http.post<BaseResponse>(`${environment.api}/action-requests`, body);
  }

  // public submitDoctorAppointment(body: AppointmentRequest) {
  //   return this.http.post<BaseResponse>(`${environment.api}/medical-check`, body);
  // }

  public submitCheckupService(body: CheckupRequest) {
    return this.http.post<BaseResponse>(`${environment.api}/medical-check`, body);
  }

  public getDoctorSpecializations() {
    return this.http.get(`${environment.api}/choices`);
  }

  public getPrescriptions(): Observable<BaseResponse> {
    return this.http.get<BaseResponse>(`${environment.api}/prescription-request`);
  }

  public createPrescription(body: FormData) {
    return this.http.post<BaseResponse>(`${environment.api}/prescription-request`, body);
  }

  public getCalls(): Observable<BaseResponse> {
    // return this.http.post<BaseResponse>(`${environment.api}/action-requests`);
    const content: Array<any> = [];
    for (let i = 0; i < _.random(10, 20); ++i) {
      content.push(i);
    }
    return of({
      content,
      metadata: {}
    }).pipe(delay(200));
  }

  public getMedicalHistoryChoices() {
    return this.http.get<BaseResponse>(`${environment.api}/medical-history/choices`);
  }

  public submitMedicalHistory(body: any) {
    return this.http.post(`${environment.api}/medical-history`, body);
  }

  public checkMedicalHistory() {
    return this.http.get<BaseResponse>(`${environment.api}/medical-history/check`);
  }

  public getCurrentWeather(lat: number, long: number) {
    let params = new HttpParams().set('APPID', environment.openWeatherKey);
    params = params.set('lat', lat.toString());
    params = params.set('lon', long.toString());
    return this.http.get(`https://cors-anywhere.herokuapp.com/http://api.openweathermap.org/data/2.5/weather`, { params });
  }

  public getWeatherForecast(lat: number, long: number) {
    let params = new HttpParams().set('APPID', environment.openWeatherKey);
    params = params.set('lat', lat.toString());
    params = params.set('lon', long.toString());
    return this.http.get(`https://cors-anywhere.herokuapp.com/http://api.openweathermap.org/data/2.5/forecast`, { params });
  }

  public getCallsPackages() {
    return this.http.get<BaseResponse>(`${environment.api}/call-pack-list`);
  }

  public getCreditCardsList() {
    const params = new HttpParams().set('status', 'TOKEN-OK');
    return this.http.get<BaseResponse>(`${environment.api}/sim-card/list-cc`, { params });
  }

  public buySimPlan(requestBody: SimPlan) {
    return this.http.post<BaseResponse>(`${environment.api}/sim-card/buy`, requestBody);
  }

  public registerDevicePush(requestBody: RegisterDeviceFcmRequest) {
    return this.http.post<BaseResponse>(`${environment.api}/reg-device`, requestBody);
  }
}
