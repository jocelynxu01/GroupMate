import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RunTeamGeneratorComponent } from './run-team-generator.component';

describe('RunTeamGeneratorComponent', () => {
  let component: RunTeamGeneratorComponent;
  let fixture: ComponentFixture<RunTeamGeneratorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RunTeamGeneratorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RunTeamGeneratorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
