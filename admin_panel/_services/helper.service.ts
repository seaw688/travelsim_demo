import { Injectable } from '@angular/core';



@Injectable({ providedIn: 'root' })
export class HelperService {



    constructor() {

    }

    getProp(item: any, prop: string, subProp?: string): any {
        let resp = '';
        resp = item && item[prop] !== null ? item[prop] : '-';
        if (subProp && item[prop] !== null) {
            resp = resp[subProp];
        }

        return resp;
    }
}
