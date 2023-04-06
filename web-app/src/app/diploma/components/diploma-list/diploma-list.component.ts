import { Component, OnInit } from '@angular/core';
import {DiplomaService} from "../../service/diploma.service";
import {Diploma} from "../../model/diploma.model";
import {catchError, throwError} from "rxjs";

@Component({
  selector: 'app-diploma-list',
  templateUrl: './diploma-list.component.html',
  styleUrls: ['./diploma-list.component.css']
})
export class DiplomaListComponent implements OnInit {

  public diplomas: Diploma[] = [];
  displayedColumns = ['position', 'title', 'dateOfDefence', 'diplomaType'];

  constructor(private diplomaService: DiplomaService) { }

  ngOnInit(): void {
    this.getDiplomas();
  }

  public getDiplomas(): void {
    this.diplomaService.getDiplomas().pipe(
      catchError(err => {
        return throwError(err);
      })
    ).subscribe(data => {
      this.diplomas = data;
    });

  }

}
