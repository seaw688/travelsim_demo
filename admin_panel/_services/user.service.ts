import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Subject } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { environment } from '@environments/environment';
import { User } from '@app/_models';




@Injectable({ providedIn: 'root' })
export class UserService {

    private deletingSubject = new Subject();
    private activatingSubject = new Subject();
    private options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };
    public deleting$ = this.deletingSubject.asObservable();
    public activating$ = this.activatingSubject.asObservable();




    constructor(private http: HttpClient) { }

    getAll() {
        return this.http.get<User[]>(`${environment.apiUrl}/users`);
    }

    getAllUsers() {
        return this.http.get(`${environment.apiUrl}/users/`);
    }

    getById(id: number): any {
        return this.http.get(`${environment.apiUrl}/users/${id}`);
    }

    register(user: User) {
        return this.http.post(`${environment.apiUrl}/users/`, user);
    }

    update(user: User, id: any) {
        return this.http.patch(`${environment.apiUrl}/users/${id}/`, JSON.stringify(user), this.options).pipe(finalize(() => this.activatingSubject.next(true)));
    }

    delete(id: number) {
        return this.http.delete(`${environment.apiUrl}/users/${id}/`).pipe(finalize(() => this.deletingSubject.next(true)));
    }

}
