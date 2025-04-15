import { Component } from '@angular/core';
import { CryptographyService } from '../services/cryptography.service';

@Component({
  selector: 'app-key-generation',
  templateUrl: './key-generation.component.html',
  styleUrls: ['./key-generation.component.css']
})
interface RSAKeysResponse {
  public_key: string;
  private_key: string;
}

export class KeyGenerationComponent {

  bits: number = 512;
  publicKey: string = '';  // Changed to string
  privateKey: string = '';  // Changed to string

  constructor(private cryptoService: CryptographyService) {}

  generateKeys() {
    this.cryptoService.generateRSAKeys(this.bits).subscribe((response: RSAKeysResponse) => {
      this.publicKey = response.public_key;
      this.privateKey = response.private_key;
    });
  }
  

  saveKeys() {
    // Logic to save keys to a file or local storage
  }
}
