import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KeyGenerationComponent } from './key-generation.component';

describe('KeyGenerationComponent', () => {
  let component: KeyGenerationComponent;
  let fixture: ComponentFixture<KeyGenerationComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [KeyGenerationComponent]
    });
    fixture = TestBed.createComponent(KeyGenerationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
