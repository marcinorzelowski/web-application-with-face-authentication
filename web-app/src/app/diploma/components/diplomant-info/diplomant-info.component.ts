import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../../shared/services/auth.service";
import {User} from "../../../auth/model/auth.model";

@Component({
  selector: 'app-diplomant-info',
  templateUrl: './diplomant-info.component.html',
  styleUrls: ['./diplomant-info.component.css']
})
export class DiplomantInfoComponent implements OnInit {
  public user!: User | null
  constructor(private authService: AuthService) { }

  ngOnInit(): void {
    this.user = this.authService.user$.value;
  }

}
