import { Component, OnInit } from '@angular/core';
import {Diploma} from "../../model/diploma.model";
import {DiplomaService} from "../../service/diploma.service";

@Component({
  selector: 'app-diploma-container',
  templateUrl: './diploma-container.component.html',
  styleUrls: ['./diploma-container.component.css']
})
export class DiplomaContainerComponent implements OnInit {

  public diploma!: Diploma
  constructor(private diplomaService: DiplomaService) { }

  ngOnInit(): void {
    this.diplomaService.getDiploma().subscribe(data => {
      this.diploma = data;
    })
  }

}
