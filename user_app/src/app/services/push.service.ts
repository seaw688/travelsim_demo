import { Injectable } from '@angular/core';

import { OneSignal } from '@ionic-native/onesignal/ngx';
import { UniqueDeviceID } from '@ionic-native/unique-device-id/ngx';

import { ApiService } from 'src/app/services/api.service';

import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PushService {

  constructor(private oneSignal: OneSignal, private uniqueDeviceID: UniqueDeviceID, private api: ApiService) { }

  private userId: string;
  private deviceId: string;

  public async initOneSignal() {
    this.oneSignal.startInit(environment.oneSignalAppID, environment.firebaseSenderID);
    this.oneSignal.endInit();
    this.userId = (await this.oneSignal.getIds()).userId;
    this.deviceId = await this.uniqueDeviceID.get();
  }

  public registerDevicePush() {
    this.api.registerDevicePush({player_id: this.userId, device_id: this.deviceId}).subscribe(
      res => console.log(res),
      err => console.log(err)
    );
  }
}
