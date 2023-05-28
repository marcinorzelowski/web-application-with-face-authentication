import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DiplomaRoutingModule } from './diploma-routing.module';
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatButtonModule} from "@angular/material/button";
import { DiplomaContainerComponent } from './components/diploma-container/diploma-container.component';
import {MatCardModule} from "@angular/material/card";
import {MatDividerModule} from "@angular/material/divider";
import {MatListModule} from "@angular/material/list";
import {MatTableModule} from "@angular/material/table";


@NgModule({
  declarations: [


    DiplomaContainerComponent,

  ],
  imports: [
    CommonModule,
    DiplomaRoutingModule,
    MatToolbarModule,
    MatButtonModule,
    MatCardModule,
    MatDividerModule,
    MatListModule,
    MatTableModule
  ]
})
export class DiplomaModule { }
