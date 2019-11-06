import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable, Subject, from } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';

import { BaseResponse, Language } from 'src/app/models/models';

import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LanguageService {

  private languageIsLoadedSubject: Subject<boolean> = new Subject();
  public languageIsLoaded$: Observable<boolean> = this.languageIsLoadedSubject.asObservable();

  private _language: any;

  constructor(private http: HttpClient) { }

  public set language(language: any) {
    this._language = language;
  }

  public get language() {
    return this._language;
  }

  public loadLanguage(language: string = 'En') {
    const params = new HttpParams().append('title', language);
    this.http.get<BaseResponse>(`${environment.api}/language`, { params })
      .pipe(
        map((res: BaseResponse) => res.content),
        switchMap((res: Array<Language>) => {
          const parts = res[0].file_url.split('/');
          const fileName = parts[parts.length - 1];
          return from(fetch(`https://www.travelsim.tk/media/language/${fileName}`).then(resp => resp.json()));
        })
      )
      .subscribe((res: any) => {
        this.language = res;
        this.languageIsLoadedSubject.next(true);
      });
  }

  public getTextByCategories(category?: string) {
    if (this.language) {
      return category ? { ...this.language.common, ...this.language[category] } : { ...this.language.common };
    }
    return {};
  }
}
