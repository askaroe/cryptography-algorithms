import { Component } from '@angular/core';
import { RsaService } from '../rsa.service';

@Component({
  selector: 'app-rsa',
  templateUrl: './rsa.component.html',
  styleUrls: ['./rsa.component.css']
})
export class RsaComponent {
  publicKey = '';
  privateKey = '';
  message = '';
  encryptedText = '';
  decryptedText = '';

  constructor(private rsaService: RsaService) {}

  generateKeys() {
    this.rsaService.generateKeys().subscribe(data => {
      this.publicKey = data.public_key;
      this.privateKey = data.private_key;
    });
  }

  encryptMessage() {
    this.rsaService.encryptMessage(this.message).subscribe(data => {
      this.encryptedText = data.ciphertext;
    });
  }

  decryptMessage() {
    this.rsaService.decryptMessage(this.encryptedText).subscribe(data => {
      this.decryptedText = data.message;
    });
  }

  saveKeys() {
    this.rsaService.saveKeys(this.publicKey, this.privateKey).subscribe(response => {
      alert(response.message);
    });
  }

  saveEncrypted() {
    this.rsaService.saveEncrypted(this.encryptedText).subscribe(response => {
      alert(response.message);
    });
  }

  saveDecrypted() {
    this.rsaService.saveDecrypted(this.decryptedText).subscribe(response => {
      alert(response.message);
    });
  }
}
