import { Component, OnInit } from '@angular/core';
import {Observable, Subject} from "rxjs";
import {MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-camera',
  templateUrl: './camera.component.html',
  styleUrls: ['./camera.component.css']
})
export class CameraComponent implements OnInit {
  public image!: string | null;
  private trigger: Subject<void> = new Subject<void>();
  public triggerObservable: Observable<void> = this.trigger.asObservable();
  private file!: File;

  constructor(private dialogRef: MatDialogRef<CameraComponent>) { }

  capture() {
    this.trigger.next();
  }

  onImageCapture(event: any) {

    this.image = event.imageAsDataUrl;


    fetch(event.imageAsDataUrl)
      .then(response => response.arrayBuffer())
      .then(buffer => {
        const blob = new Blob([buffer], { type: 'image/jpeg' });
        this.file = new File([blob], 'image.jpeg', { type: 'image/jpeg' });
      })
      .catch(error => {
        console.error('Error converting base64 to Blob:', error);
      });
  }

  public onCreateNewOne() {
    this.image = null;
  }

  public onSave(): void {
    this.dialogRef.close(this.file)
  }

  ngOnInit(): void {
  }

  cancel() {
    this.dialogRef.close(null);
  }
}
