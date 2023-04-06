import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {AuthGuard} from "../shared/guards/auth.guard";
import {DiplomaContainerComponent} from "./components/diploma-container/diploma-container.component";

const routes: Routes = [
  {path: '', canActivate: [AuthGuard], component: DiplomaContainerComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DiplomaRoutingModule { }
