import { Injectable } from '@angular/core';

import { Storage } from '@ionic/storage';

import { Observable, from } from 'rxjs';
import { switchMap, map } from 'rxjs/operators';

import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class StorageService {

  constructor(private storage: Storage) { }

  private _lastUrl = '/login';

  public get lastUrl() {
    return this._lastUrl;
  }

  public set lastUrl(url: string) {
    this._lastUrl = url;
  }

  set<T>(key: string, value: any): Observable<T> {
    if (!key) {
      throw Error('argument "key" is required');
    }
    if (!value) {
      throw Error('argument "value" is required');
    }

    return from(this.storage.set(this.key(key), JSON.stringify(value))).pipe(switchMap(() => this.get(key)));
  }

  get<T>(key: string): Observable<T> {
    if (!key) {
      throw Error('argument "key" is required');
    }
    return from(this.storage.get(this.key(key))).pipe(map(res => JSON.parse(res)));
  }

  getBase<T>(key: string): Observable<T> {
    if (!key) {
      throw Error('argument "key" is required');
    }
    return from(this.storage.get(this.key(key))).pipe(map(res => JSON.parse(res)['content']));
  }

  remove<T>(key: string): Observable<any> {
    if (!key) {
      throw Error('argument "key" is required');
    }
    return from(this.storage.remove(this.key(key)));
  }

  key(key: string): string {
    return `${environment.storage}_${key}`;
  }
}
