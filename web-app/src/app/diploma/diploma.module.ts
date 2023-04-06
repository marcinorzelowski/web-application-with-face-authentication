import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DiplomaRoutingModule } from './diploma-routing.module';
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatButtonModule} from "@angular/material/button";
import { DiplomaContainerComponent } from './components/diploma-container/diploma-container.component';
import {MatCardModule} from "@angular/material/card";
import { DiplomantInfoComponent } from './components/diplomant-info/diplomant-info.component';
import { DiplomaListComponent } from './components/diploma-list/diploma-list.component';
import {MatDividerModule} from "@angular/material/divider";
import {MatListModule} from "@angular/material/list";
import {MatTableModule} from "@angular/material/table";


@NgModule({
  declarations: [


    DiplomaContainerComponent,
      DiplomantInfoComponent,
      DiplomaListComponent
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
