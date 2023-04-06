import { Component, OnInit } from '@angular/core';
import {User} from "../../../auth/model/auth.model";
import {AuthService} from "../../services/auth.service";

@Component({
  selector: 'app-top-menu',
  templateUrl: './top-menu.component.html',
  styleUrls: ['./top-menu.component.css']
})
export class TopMenuComponent implements OnInit {

  public user!: User | null
  constructor(private authService: AuthService) { }

  ngOnInit(): void {
    this.setUser();
  }

  public setUser() {
    this.authService.user$.subscribe(x => this.user = x)
  }

  logout() {
    this.authService.logout();
  }

}
