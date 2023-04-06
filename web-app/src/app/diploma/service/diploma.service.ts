import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Diploma} from "../model/diploma.model";

@Injectable({
  providedIn: 'root'
})
export class DiplomaService {

  constructor(private httpClient: HttpClient) { }

  public getDiplomas(): Observable<Diploma[]> {
    return this.httpClient.get<Diploma[]>('http://localhost:8080/api/diploma');
  }
}
