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
  public webcamOptions: MediaTrackConstraints = {
    width: 1280,
    height: 720
  };
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

  protected onCreateNewOne() {
    this.image = null;
  }
  async addImage(event: any) {
    const target = event.target as HTMLInputElement;
    if (target.files) {
      this.file = target.files[0];
      try {
        this.image = await this.convertFileToBase64(this.file) as string
      } catch (error) {
        console.error('Failed to convert file to base64.')
      }
    }
  }

  public onSave(): void {
    this.dialogRef.close(this.file)
  }

  ngOnInit(): void {
  }

  convertFileToBase64(file: File): Promise<string | ArrayBuffer | null> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
      reader.readAsDataURL(file);
    });
  }

  cancel() {
    this.dialogRef.close(null);
  }
}
