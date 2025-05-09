import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassFeedComponent } from './class-feed.component';

describe('ClassFeedComponent', () => {
  let component: ClassFeedComponent;
  let fixture: ComponentFixture<ClassFeedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClassFeedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ClassFeedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
